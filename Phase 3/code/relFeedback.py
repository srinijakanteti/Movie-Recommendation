
def relFeedback(QVect,R,I):
    n1 = len(R)
    n2 = len(I)
    n = n1+n2
    sum_r = []
    sum_i = []
    QVect1 = []
    qLen = len(QVect)
    for p in range(qLen):
        sum_r.append(0)
        sum_i.append(0)
        QVect1.append(0)
    for i in range(n1):
        R1 = R[i]
        for m in range(qLen):
            sum_r[m] += R1[m]
    #print(sum_r)
    for j in range(n2):
        I1 = I[j]
        for m in range(qLen):
            sum_i[m] += I1[m]
    #print(sum_i)
    for k in range(qLen):
        QVect1[k] = QVect[k] + (sum_r[k] - sum_i[k])/n
    return QVect1

