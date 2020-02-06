"""=========================================================================================
	這是武漢肺炎的例子 , 資料出處 可參考 ~ https://www.ptt.cc/bbs/Gossiping/M.1580941400.A.B3E.html

==============================================================================================="""
import matplotlib.pyplot as plt
import numpy as np
import json


#================================================================================
# 自行定義基底 !!! 
def c_func(x):
	return 1
def x_func(x):
	return x

def x2_func(x):
	return x**2
def x3_func(x):
	return x**3

#=================================================================================

def basis(x):
	return np.array([c_func(x),x_func(x),x2_func(x),x3_func(x)]).reshape(-1,1)


def model(w,x):
	return (np.transpose(w)@ basis(x)).item()



if __name__ == '__main__':
	with open("2019_nCoV.json",encoding='utf8') as f: 
		j = json.load(f)
	xdata = j['天數']
	ytarget = j['累積確診人數']
	ypred = []
	#===================================================================================
	# compute A-inverse 
	n = len(xdata)
	A = np.zeros((4,4))
	b = np.zeros((4,1))
	for i in range(n):
		phi = basis(xdata[i])
		phiT = np.transpose(phi)
		A+= phi @ phiT
		b += ytarget[i]*phi
	invA = np.linalg.inv(A)	
	# compute w
	w = (invA @ b).reshape(-1)
	#======================================================================================
	# compute r2 
	res = 0.0
	mu = np.mean(ytarget)
	tot = 0.0
	for i in range(n):
		predval = model(w,xdata[i])
		ypred.append(predval)
		res += (ytarget[i] - predval)**2
		tot += (ytarget[i] - mu)**2
	r2 = 1-res/tot
	print("w:{}".format(w))
	print("r2:{}".format(r2))
	#======================================================================================
	plt.title("2019-nCoV")
	plt.xlabel("day")
	plt.ylabel("# counts")
	plt.scatter(xdata,ytarget,marker='o',color='r',label="target")
	plt.plot(xdata,ypred,linestyle='--',color='g',label="pred_line")
	plt.scatter(xdata,ypred,marker='x',color='b',label="pred")
	plt.legend()
	plt.savefig("result.png")
	plt.show()


