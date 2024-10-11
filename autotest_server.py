#auto_server.py
from flask import Flask, request, redirect, url_for, render_template, session, jsonify, send_from_directory
import os
import subprocess
from celery_app import make_celery
from Android_Test import AndroidTest
from pathlib import Path
import csv
from atc_kine_push_vc import AtcKinePushVc
from atc_kine_push_rg import AtcKinePushRg
from atc_mix_vc import AtcMixVc
from atc_mix_rg import AtcMixRg

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# 폴더 설정 (파일이 저장된 폴더)
FOLDER_PATH = 'uploads'
os.makedirs(FOLDER_PATH, exist_ok=True)
app.config['FOLDER_PATH'] = FOLDER_PATH

RESULT_FOLDER = 'Result'
os.makedirs(RESULT_FOLDER, exist_ok=True)
app.config['RESULT_FOLDER'] = RESULT_FOLDER

TEST_FOLDER = 'Test'  # Test 폴더 경로 설정
os.makedirs(TEST_FOLDER, exist_ok=True)

TestCaseFilepath = f'./{TEST_FOLDER}/TestCase.csv'
FILED_NAME = ["Type", "TestCase", "Result", "Desc"]

def create_or_update_csv(file_path, fieldnames):
    # 파일이 존재하는지 확인
    file_exists = os.path.exists(file_path)

    # 파일이 없는 경우 생성
    if not file_exists:
        print(f"파일이 존재하지 않으므로 {file_path} 파일을 생성합니다.")
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()  # 필드명을 추가
        print(f"필드명이 추가되었습니다: {fieldnames}")
    else:
        # 파일이 있는 경우, 필드명이 있는지 확인하고 없으면 추가
        with open(file_path, mode='r+', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

            if len(rows) == 0 or rows[0] != fieldnames:
                print(f"필드명이 없거나 잘못되어 필드명을 추가합니다.")
                # 파일 내용을 새로 쓰기 위해 파일 포인터를 처음으로 이동
                file.seek(0)
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()  # 필드명을 첫 줄에 추가
                file.writelines([','.join(row) + '\n' for row in rows])  # 기존 내용 유지
                print(f"필드명이 추가되었습니다: {fieldnames}")
            else:
                print(f"필드명이 이미 존재합니다: {fieldnames}")


# Celery 인스턴스 생성
celery = make_celery(app)

@app.route('/delete_task/<task_id>', methods=['POST'])
def delete_task(task_id):
    task_ids = session.get('task_ids', [])
    if task_id in task_ids:
        task_ids.remove(task_id)
        session['task_ids'] = task_ids
    return redirect(url_for('task_status'))
def get_connected_devices():
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, text=True)
    devices = []
    for line in result.stdout.splitlines():
        if '\tdevice' in line:
            devices.append(line.split('\t')[0])
    return devices


@celery.task(bind=True, name='autotest_server.process_files_and_text')
def process_files_and_text(self, devices,account, action, tcs,file_path1, file_path2="" ):

    current_step = 0
    fail_cnt = 0
    success_cnt = 0
    fail_str = ''
    success_str = ''
    total_steps = len(tcs) * len(devices)
    test = AndroidTest(action,account = account, version1=file_path1, version2=file_path2)


    for subtc in tcs:


        for device in devices:
            # 각각의 디바이스에 작업을 처리합니다
            print(
                f"process_files_and_text action :{action}, device: {device},TCS:{tcs} ,file_path1: {file_path1},path2: {file_path2} {len(tcs)}")
            print(f"process_files_and_text subtc {subtc}")
            test.set_device(device)
            test.set_subTC(subtc)
            # return {'result': f"subTC : {test.subTC} type: {test.test_type} ori subtc{subtc}"}

            current_step += 1
            retvalue = test.perform_actions()
            if retvalue == True:
                success_cnt += 1
                if success_str == '':
                    success_str = f"{{ Success : {success_cnt}, TC : {action}, SubTC : {subtc}, device : {device} Version1 : {Path(file_path1).name}, version2 : {Path(file_path2).name} }}"
                else:
                    success_str = f"{success_str}, {{ Success : {success_cnt}, TC : {action}, SubTC : {subtc}, device : {device} Version1 : {Path(file_path1).name}, version2 : {Path(file_path2).name} }}"
            else:
                fail_cnt += 1
                if fail_str == '':
                    fail_str = f"{{ Fail : {fail_cnt}, TC : {action}, SubTC : {subtc}, device : {device} Version1 : {Path(file_path1).name}, version2 : {Path(file_path2).name} }}"
                else:
                    fail_str = f"{fail_str}, {{ Fail : {fail_cnt}, TC : {action}, SubTC : {subtc}, device : {device} Version1 : {Path(file_path1).name}, version2 : {Path(file_path2).name} }}"
            self.update_state(state='PROGRESS', meta={'current': current_step, 'total': total_steps, 'success_cnt': success_cnt, 'fail_cnt': fail_cnt, 'status': f'Processing step {current_step}'})

            devices_str = ', '.join(devices)
    return {'result': f"Total : {total_steps} Success Count: {success_cnt} result path = http://127.0.0.1:5000/images/{test.result_folder}"}


def read_csv_file(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        csv_content = []
        for row in reader:
            csv_content.append(row)
        return csv_content

@app.route('/')
def index():


    create_or_update_csv(TestCaseFilepath, FILED_NAME)

    apk_files = get_apk_files(FOLDER_PATH)
    devices = get_connected_devices()  # 디바이스 목록 가져오기
    # subfolders, subfolder_files = get_subfolders(TEST_FOLDER)  # 서브폴더 및 파일 가져오기
    test_cases = []
    with open(TestCaseFilepath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            test_cases.append(row)

    return render_template('index.html', apk_files=apk_files, devices=devices, test_cases=test_cases)
# @app.route('/')
# def index():
#     files = os.listdir(FOLDER_PATH)
#     devices = get_connected_devices()
#     subfolders, subfolder_files = get_subfolders(TEST_FOLDER)
#     return render_template('index.html', files=files, devices=devices, subfolders=subfolders, subfolder_files=subfolder_files)

@app.route('/upload_apk', methods=['POST'])
def upload_apk():
    if 'file1' not in request.files:
        return "테스트 APK를 선택하세요."
    file1 = request.files['file1']

    # 다음 서브 폴더 번호를 결정하고 폴더 생성
    # next_folder_number = get_next_folder_number(TEST_FOLDER)
    # new_folder_path = os.path.join(TEST_FOLDER, f'TC{next_folder_number}')
    # os.makedirs(new_folder_path, exist_ok=True)

    # 파일을 새 폴더에 저장
    filepath1 = os.path.join(FOLDER_PATH, file1.filename)
    file1.save(filepath1)

    return redirect(url_for('index'))

@app.route('/upload_TC', methods=['POST'])
def upload_TC():

    test_type = request.form['test_type']
    if test_type =='mix':
        if 'mixurl' not in request.form or 'tcresultfile' not in request.files or 'tcdesc' not in request.form:
            return "Mix url 선택 하고  TC 설명을 입력 하세요.."
        tcurl = request.form['mixurl']
        tc = os.path.basename(tcurl)

    elif test_type =='kine':
        if 'tckinefile' not in request.files or 'tcresultfile' not in request.files or 'tcdesc' not in request.form:
            return "TC 파일 및 결과 파일을 선택 하고  TC 설명을 입력 하세요.."
        tcfile = request.files['tckinefile']
        tc=os.path.splitext(tcfile.filename)[0]
        if os.path.splitext(tcfile.filename)[1].lower() != '.kine':
            return "Kine 파일을 선택하세요."

    else:
        return "잘못된 테스트 타입입니다."

    tcresultfile= request.files['tcresultfile']
    tcdesc = request.form['tcdesc']

    # Kine 파일을 새 폴더에 저장
    if test_type == 'kine':
        kine_filepath = os.path.join(TEST_FOLDER , f'{tc}.kine')
        tcfile.save(kine_filepath)
    result_filepath = os.path.join(TEST_FOLDER, f'{tc}.mp4')
    tcresultfile.save(result_filepath)

    FILED_NAME = ["Type", "TestCase", "Result", "Desc"]

    if test_type =='mix':
        row_data = {'Type': test_type, 'TestCase': tcurl, 'Result': f'{tc}.mp4',"Desc":tcdesc}
    elif test_type == 'kine':
        row_data = {'Type': test_type, 'TestCase': f'{tc}.kine', 'Result': f'{tc}.mp4', "Desc": tcdesc}

    with open(TestCaseFilepath, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=FILED_NAME)

        # 행 추가
        writer.writerow(row_data)

    # 설명을 텍스트 파일로 저장

    return redirect(url_for('index'))

@app.route('/upload_files', methods=['POST'])
def upload_files():
    selected_files = request.form.getlist('files')
    devices = request.form.getlist('devices')
    action = request.form.get('action')
    tcs = request.form.getlist('range')
    account = request.form['account']


    num_devices = len(devices)
    if not action:
        return "Please select TC"

    if action == "versioncompare":
        if len(selected_files) != 2 or num_devices == 0 or not action:
            return f"Please select exactly 2 files, at least one device, and an action. len(selected_files)={len(selected_files)}, num_devices={num_devices}, TC={action}"
        file_path1 = os.path.join(FOLDER_PATH, selected_files[0])
        file_path2 = os.path.join(FOLDER_PATH, selected_files[1])
        # return f"file_path1 {file_path1} file_path2 {file_path2}"
        # tc_numbers = [int(tc.replace('TC', '')) for tc in tcs]
        # 작업 태스크 시작def process_files_and_text(self, devices,account, action, tcs,file_path1, file_path2="" ):
        task = process_files_and_text.apply_async(args=[devices, account,action, tcs,file_path1, file_path2])
    elif action == "regression":
        if len(selected_files) != 1 or num_devices == 0 or not action:
            return f"Please select exactly 1 files, at least one device, and an action. len(selected_files)={len(selected_files)}, num_devices={num_devices}, TC={action}"
        file_path1 = os.path.join(FOLDER_PATH, selected_files[0])
        # return f"file_path1 {file_path1} file_path2 {file_path2}"
        # 작업 태스크 시작
        task = process_files_and_text.apply_async(args=[devices, account, action, tcs, file_path1])
    # 작업 ID를 세션에 추가
    task_ids = session.get('task_ids', [])
    task_ids.append(task.id)
    session['task_ids'] = task_ids

    return redirect(url_for('task_status'))

@app.route('/task_status')
def task_status():
    task_ids = session.get('task_ids', [])
    tasks = [{'id': task_id, 'task': process_files_and_text.AsyncResult(task_id)} for task_id in task_ids]
    return render_template('task_status.html', tasks=tasks)

@app.route('/task_detail/<task_id>')
def task_detail(task_id):
    task = process_files_and_text.AsyncResult(task_id)
    return render_template('task_detail.html', task=task)

# @app.route('/task_status/<task_id>')
# def task_status(task_id):
#     task = process_files_and_text.AsyncResult(task_id)
#     response = {
#         'state': task.state,
#         'current': 0,
#         'total': 1,
#         'status': 'Pending...',
#     }
#
#     if task.info is not None:
#         response.update(task.info)
#
#     return jsonify(response)
def get_apk_files(folder_path):
    apk_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.apk'):
                apk_files.append(os.path.relpath(os.path.join(root, file), folder_path))
    return apk_files
def get_image_files(folder_path):
    image_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
                image_files.append(os.path.relpath(os.path.join(root, file), folder_path))
    return image_files

@app.route('/images')
def list_images():
    subfolders = [f.name for f in os.scandir(RESULT_FOLDER) if f.is_dir()]
    return render_template('images.html', subfolders=subfolders)

@app.route('/images/<path:subfolder>')
def list_images_in_subfolder(subfolder):
    folder_path = os.path.join(RESULT_FOLDER, subfolder)
    images = get_image_files(folder_path)
    return render_template('image_list.html', images=images, subfolder=subfolder)

@app.route('/result/<path:filename>')
def result_file(filename):
    return send_from_directory(RESULT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)