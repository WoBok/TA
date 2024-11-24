import pymel.core as pm

# Make a new window
#
window = pm.window(title="Long Name", iconName='Short Name', widthHeight=(200, 55))
pm.columnLayout(adjustableColumn=True)
# Result: ui.ColumnLayout('window1|columnLayout98') #
pm.button(label='Do Nothing', command="print('Do Nothing')")
# Result: ui.Button('window1|columnLayout98|button111') #
pm.button(label='Close', command=('pm.deleteUI(\"' + window + '\", window=True)'))
# Result: ui.Button('window1|columnLayout98|button112') #
pm.setParent('..')
# Result: u'' #
pm.showWindow(window)

# Resize the main window
#

# This is a workaround to get MEL global variable value in Python
gMainWindow = maya.mel.eval('$tmpVar=$gMainWindow')
pm.window(gMainWindow, edit=True, widthHeight=(900, 777))
# Result: ui.Window('MayaWindow') #
