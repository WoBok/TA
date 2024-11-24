import pymel.core as pm

def defaultButtonPush(*args):
  print (args)

pm.window( width=150 )
# Result: ui.Window('window1') #
pm.columnLayout( adjustableColumn=True )
# Result: ui.ColumnLayout('window1|columnLayout10') #
pm.button( label='Button 1', command=defaultButtonPush )
# Result: ui.Button('window1|columnLayout10|button5') #
pm.button( label='Button 2' )
# Result: ui.Button('window1|columnLayout10|button6') #
pm.button( label='Button 3' )
# Result: ui.Button('window1|columnLayout10|button7') #
pm.button( label='Button 4' )
# Result: ui.Button('window1|columnLayout10|button8') #
pm.showWindow()