import pymel.core as pm

joint_radius = 0.05  #关节大小
bone_length = 0.5  #骨骼长度


def update_exp(exp_str):
    import maya.mel as mel
    mel_cmd = f'expression -s "{exp_str}"  -o "" -n "exp" -ae 1 -uc all ;'
    mel.eval(mel_cmd)


def initialize_exp(selected_obj):
    selected_obj_rot = selected_obj.getRotation()
    exp_str = ''
    exp_str += f'$selectedObjRotX = {selected_obj_rot.x};\\n'  #缓存被选择物体的初始角度
    exp_str += f'$selectedObjRotY = {selected_obj_rot.y};\\n'
    exp_str += f'$selectedObjRotZ = {selected_obj_rot.z};\\n'
    return exp_str


def create_joint_pair(face, parent):
    face_points = face.getPoints(space='world')  #获得当前面的所有顶点
    face_position = sum([p for p in face_points]) / len(face_points)  #计算被选择面的中心位置
    jnt1 = pm.joint(p=face_position, rad=joint_radius)
    pm.parent(jnt1, parent)

    face_normal = face.getNormal(space='world')  #获得当前面的法线
    jnt2_position = face_position + face_normal * bone_length  #当前面的位置加上法线方向的偏移得到joint 2的位置
    jnt2 = pm.joint(p=jnt2_position, rad=joint_radius)
    #jnt1.orientJoint('xyz',secondaryAxisOrient='yup')

    pm.select(clear=True)

    return jnt1.shortName()


def create_exp(jnt_name, selected_obj_name):
    exp_str = ''
    for axis in ['X', 'Y', 'Z']:
        exp_str += f'{jnt_name}.rotate{axis} = -({selected_obj_name}.rotate{axis} - $selectedObjRot{axis});\\n'  #根据被选择物体的当前角度和缓存角度计算joint的旋转
    return exp_str


def create_bones(faces):
    if not faces:  #若faces为空或选择的不是面，则不执行
        return
    if not type(faces[0]) is pm.general.MeshFace:
        return

    pm.select(clear=True)

    selected_obj = faces[0].node().getParent()
    selected_obj_name = selected_obj.name()

    exp_str = initialize_exp(selected_obj)  #初始化表达式

    joints = pm.group(n="joints")  #joint的父节点

    for face in faces:
        jnt1_name = create_joint_pair(face, joints)  #创建骨骼
        exp_str += create_exp(jnt1_name, selected_obj_name)  #为新创建的joint添加表达式

    update_exp(exp_str)  #更新表达式


faces = pm.selected(flatten=True)
create_bones(faces)  #创建所选择面的骨骼
