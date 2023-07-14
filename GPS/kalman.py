import ulab as np

def kalman(pre_lat,pre_lon,lat,lon,Vx,Vy):
    F = np.eye(2)
    H = np.eye(2)

    u = np.array(2,1)
    u[0] = Vx
    u[1] = Vy

    z = np.array(2,1)#GPSから取得した実際の観測値
    z[0] = lat
    z[1] = lon

    dlen = 1 #ノイズデータのデータ長
    mean = 0.0  #ノイズの平均値
    std  = 1.0  #ノイズの分散
    W = np.array(2,2)#ノイズ
    V = np.array(2,2)#瞬間の速度ベクトルV = (Vx,Vy)
    W[0][0] = np.random.normal(mean,std,dlen)
    W[1][1] = np.random.normal(mean,std,dlen)
    V[0][0] = np.random.normal(mean,std,dlen)
    V[1][1] = np.random.normal(mean,std,dlen)
    Q = np.cov(u)#共分散行列。入力にたいする不確かさで表される
    R = np.cov(z)#共分散行列。観測に対する不確かさを表した行列で表される。

    xAct = np.array(2,1)#ノイズを受けた実際の位置
    xRst = np.array(2,1)#推定した位置
    P = np.eye(2)#出力zの誤差共分散
#--------予測ステップ----------
    xEst = F@xEst + u
    P = F@P@F.T + Q
#-----------------------------
#--------更新ステップ----------
    y = z - H@xEst
    S = R + H@P@H.T
    K = P@H.T/S
    xEst = xEst + K@y
    P = (np.eye(2)-K@H)@P
    return xEst
