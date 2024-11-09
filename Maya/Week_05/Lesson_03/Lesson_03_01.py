import pymel.core as pm
for s in pm.selected(flatten=True):#maya将选中点根据索引打包返回，使用flatten参数可以返回所有单独的点
    print(s)
    print(s.connectedEdges())#返回点所连接的线
    print(s.connectedFaces())#返回点所连接的线
    print(s.connectedVertices())#返回点所连接的点（应该是与其组成三角面的点）
    print(s.isConnectedTo(pm.MeshVertex('pSphere1.vtx[230]')))#判断是否与某点相连
    print(s.setPosition(pm.dt.Point(1,2,2),space='world'))#设置位置
    #...
    #查看pymel.core.general.MeshVertex
    #Edge、Face中可以判断长度和面积,getUVArea,index...

pm.MeshFace('pSphere1.f[100]').select()#选择对应面
pm.PyNode('pSphere1.f[101]').select()