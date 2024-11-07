import pymel.core as pm

root_joint = pm.PyNode("joint1")

all_joints = root_joint.getChildren(ad=True)
all_joints.insert(0, root_joint)
all_joints = sorted(all_joints, key=lambda joint: len(joint.longName()))

for joint in all_joints:
    if not pm.hasAttr(joint, "level"):
        pm.addAttr(joint, ln="level", at="long", dv=0, k=1)
    if not pm.hasAttr(joint, "trunkId"):
        pm.addAttr(joint, ln="trunkId", at="long", dv=0, k=1)
    if not pm.hasAttr(joint, "tag"):
        pm.addAttr(joint, ln="tag", at="enum", en="leaf:trunk:branch", k=1)

all_joints[0].tag.set(1)

for joint in all_joints[1:]:
    joint.tag.set(min(len(joint.getChildren()), 2))

    jointParent = joint.getParent()

    jointParentLevel = jointParent.level.get()
    jointParentTrunkId = jointParent.trunkId.get()
    if joint.tag.get() == 2:
        joint.level.set(jointParentLevel + 1)
        joint.trunkId.set(0)
    else:
        joint.level.set(jointParentLevel)
        joint.trunkId.set(jointParentTrunkId + 1)


# --------------------------------------------
# for joint in all_joints:
#     if pm.hasAttr(joint, "level"):
#         pm.deleteAttr(joint, at="level")
#     if pm.hasAttr(joint, "trunkId"):
#         pm.deleteAttr(joint, at="trunkId")
#     if pm.hasAttr(joint, "tag"):
#         pm.deleteAttr(joint, at="tag")
