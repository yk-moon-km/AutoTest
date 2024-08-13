#auto_server.py
from flask import Flask, request, redirect, url_for, render_template, session, jsonify, send_from_directory
import os
import subprocess
from celery_app import make_celery
from Android_Test import AndroidTest
from pathlib import Path

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

def get_subfolders(folder):
    subfolders = [f.name for f in os.scandir(folder) if f.is_dir()]
    subfolder_files = {}
    for subfolder in subfolders:
        files = []
        subfolder_path = os.path.join(folder, subfolder)
        for file in os.listdir(subfolder_path):
            file_path = os.path.join(subfolder_path, file)
            if os.path.isfile(file_path):
                if os.path.splitext(file_path)[1].lower() == '.txt':
                    with open(file_path, 'r') as f:
                        files.append({'name': file, 'content': f.read()})
        subfolder_files[subfolder] = files
    return subfolders, subfolder_files

def get_next_folder_number(base_folder):
    subfolders = get_subfolders(base_folder)[0]
    numbers = [int(subfolder.replace('TC', '')) for subfolder in subfolders if subfolder.startswith('TC') and subfolder.replace('TC', '').isdigit()]
    return max(numbers, default=0) + 1

@celery.task(bind=True, name='autotest_server.process_files_and_text')
def process_files_and_text(self, devices,account, action, tcs,file_path1, file_path2="" ):
    import time

    current_step = 0
    fail_cnt = 0
    success_cnt = 0
    fail_str = ''
    success_str = ''
    total_steps = len(tcs) * len(devices)
    test = AndroidTest(action,account = account, version1=file_path1, version2=file_path2)


    for device in devices:
        print(f"{action}, {device} ,{file_path1},{file_path2}")
        test.test_seting(action, account,device, file_path1, file_path2)
        for count in tcs:
            # 각각의 디바이스에 작업을 처리합니다
            current_step += 1
            retvalue = test.perform_actions(count)
            if retvalue == True:
                success_cnt += 1
                if success_str == '':
                    success_str = f"{{ Success : {success_cnt}, TC : {action}, SubTC : TC{count}, device : {device} Version1 : {Path(file_path1).name}, version2 : {Path(file_path2).name} }}"
                else:
                    success_str = f"{success_str}, {{ Success : {success_cnt}, TC : {action}, SubTC : TC{count}, device : {device} Version1 : {Path(file_path1).name}, version2 : {Path(file_path2).name} }}"
            else:
                fail_cnt += 1
                if fail_str == '':
                    fail_str = f"{{ Fail : {fail_cnt}, TC : {action}, SubTC : TC{count}, device : {device} Version1 : {Path(file_path1).name}, version2 : {Path(file_path2).name} }}"
                else:
                    fail_str = f"{fail_str}, {{ Fail : {fail_cnt}, TC : {action}, SubTC : TC{count}, device : {device} Version1 : {Path(file_path1).name}, version2 : {Path(file_path2).name} }}"
            self.update_state(state='PROGRESS', meta={'current': current_step, 'total': total_steps, 'success_cnt': success_cnt, 'fail_cnt': fail_cnt, 'status': f'Processing step {current_step}'})

    devices_str = ', '.join(devices)
    return {'result': f"Total : {total_steps} Success Count: {success_cnt} result path = http://127.0.0.1:5000/images/{test.result_folder}"}

@app.route('/')
def index():
    apk_files = get_apk_files(FOLDER_PATH)
    devices = get_connected_devices()  # 디바이스 목록 가져오기
    subfolders, subfolder_files = get_subfolders(TEST_FOLDER)  # 서브폴더 및 파일 가져오기
    return render_template('index.html', apk_files=apk_files, devices=devices, subfolders=subfolders, subfolder_files=subfolder_files)
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
    if 'tcfile' not in request.files or 'tcresultfile' not in request.files or 'tcdesc' not in request.form:
        return "TC 파일 및 결과 파일을 선택 하고  TC 설명을 입력 하세요.."
    tcfile = request.files['tcfile']
    tcresultfile= request.files['tcresultfile']
    tcdesc = request.form['tcdesc']

    if os.path.splitext(tcfile.filename)[1].lower() != '.kine':
        return "Kine 파일을 선택하세요."

    # 다음 서브 폴더 번호를 결정하고 폴더 생성
    next_folder_number = get_next_folder_number(TEST_FOLDER)
    new_folder_path = os.path.join(TEST_FOLDER, f'TC{next_folder_number}')
    os.makedirs(new_folder_path, exist_ok=True)
    os.makedirs(new_folder_path + "/kine", exist_ok=True)
    os.makedirs(new_folder_path + "/mp4", exist_ok=True)

    # Kine 파일을 새 폴더에 저장
    kine_filepath = os.path.join(new_folder_path + "/kine", f'TC{next_folder_number}.kine')
    tcfile.save(kine_filepath)

    result_filepath = os.path.join(new_folder_path + "/mp4", f'TC{next_folder_number}.mp4')
    tcresultfile.save(result_filepath)

    # 설명을 텍스트 파일로 저장
    desc_filepath = os.path.join(new_folder_path, f'TC{next_folder_number}.txt')
    with open(desc_filepath, 'w') as desc_file:
        desc_file.write(tcdesc)

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
        tc_numbers = [int(tc.replace('TC', '')) for tc in tcs]
        # 작업 태스크 시작def process_files_and_text(self, devices,account, action, tcs,file_path1, file_path2="" ):
        task = process_files_and_text.apply_async(args=[devices, account,action, tc_numbers,file_path1, file_path2])
    elif action == "regression":
        if len(selected_files) != 1 or num_devices == 0 or not action:
            return f"Please select exactly 1 files, at least one device, and an action. len(selected_files)={len(selected_files)}, num_devices={num_devices}, TC={action}"
        file_path1 = os.path.join(FOLDER_PATH, selected_files[0])

        # return f"file_path1 {file_path1} file_path2 {file_path2}"
        tc_numbers = [int(tc.replace('TC', '')) for tc in tcs]
        # 작업 태스크 시작
        task = process_files_and_text.apply_async(args=[devices, account, action, tc_numbers, file_path1])
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