# coding=utf-8
import os

from flask import Blueprint, request
from flask import send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from koromon import settings
from koromon.exts.rbac import rbac
from koromon.upload.models import UploadFile
from koromon.utils.resp import fail, success

bp = Blueprint('upload', __name__, url_prefix='/uploads')

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_FILE_EXTENSIONS = {'txt', 'pdf', 'doc', 'xls', 'docx', 'xlsx'}


def allowed_file(file_name, file_type):
    if file_type == 'image':
        return '.' in file_name and \
               file_name.rsplit('.', 1)[1] in ALLOWED_IMAGE_EXTENSIONS
    elif file_type == 'file':
        return '.' in file_name and \
               file_name.rsplit('.', 1)[1] in ALLOWED_FILE_EXTENSIONS


@bp.route('', methods=['POST'])
@rbac.allow(['superuser', 'manager'], methods=['POST'])
@login_required
def upload():
    user = current_user
    uploading_file = request.files['file']
    upload_type = request.form.get('file_type', default='image', type=str)
    if upload_type not in ('image', 'file'):
        return fail(message=u'文件类型不正确')
    if uploading_file and allowed_file(uploading_file.filename, upload_type):
        file_name = secure_filename(uploading_file.filename)
        if UploadFile.check_file_name(file_name=file_name) is True:
            file_path = os.path.join(
                'koromon',
                settings.UPLOAD_FOLDER,
                file_name
            )
            uploading_file.save(file_path)
            actually_file_path = ''.join(['/static/Uploads/', file_name])
            UploadFile(
                file_name=file_name,
                file_path=actually_file_path,
                user_id=user.id
            ).save()
            return success(
                message=u'上传成功',
                result={
                    'file_path': actually_file_path
                }
            )
        return fail(
            message=u'文件名已存在，请重新命名文件再上传'
        )
    return fail(
        message=u'文件格式不符合要求，请上传正确格式文件'
    )
