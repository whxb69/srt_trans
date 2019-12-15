import go
import sys
import re
import os
from ui import *
from PyQt5.QtWidgets import QFileDialog
import time
import chardet

class Translate(QMainWindow):
    def open(self):
        # os.chdir('e:\\')
        FileName, filetype = QFileDialog.getOpenFileName(self,
                                                         "选取文件",
                                                         "",
                                                         "Subtitle File(*.srt);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔\
        if FileName:
            code = {}
            ui.textEdit.setText("")
            try:                                # 解码读取并识别编码
                f = open(FileName,'rb')
                text = f.read()
                code = chardet.detect(text)
                # print(code)
                ui.textEdit.setText(text)
            except:                             # 按识别到的编码读取
                # print(code['encoding'])
                f = open(FileName, encoding = code['encoding'])
                text = f.read()
                # print(text)
                ui.textEdit.setText(text)



            f.close()


    def save(self):
        FileName, filetype = QFileDialog.getSaveFileName(self,
                                                         "选取文件",
                                                         "",
                                                         "Text Files (*.txt);;Subtitle File(*.srt)")  # 设置文件扩展名过滤,注意用双分号间隔
        if FileName:
            f = open(FileName, 'w')
            f.write(ui.textEdit_2.toPlainText())
            f.close()

    def tran(self):
        fun = go.tfunction()
        text = ui.textEdit.toPlainText()        #原文本
        nodes = text.split('\n\n')
        dic = {}
        dic_n = {}
        alltxt = ''
        txt_temp = ''
        for node in nodes:
            try:
                no,stamp = node.strip().split('\n')[:2]
                txt = (' ').join(node.strip().split('\n')[2:])
            except:
                #异常项跳过 '',' \n ','\t\t\t\t'
                continue
            
            start,end = stamp.split(' --> ')
            dic[no] = {'start':start,'end':end,'txt':txt}
            pat_ws = re.compile("[^\w\s']")
            flag = pat_ws.match(txt[-1])
            txt += ' '

            #判断是否句子结束
            if not flag:#非结尾
                if  not txt_temp:
                    dic_n[len(dic_n)] = {}
                    dic_n[len(dic_n)-1]['start'] = start
                txt_temp += txt
            else:#结尾
                txt_temp += txt
                if len(dic_n) == 0 or 'end' in dic_n[len(dic_n)-1].keys():
                    dic_n[len(dic_n)] = {}
                    dic_n[len(dic_n) - 1]['start'] = start
                dic_n[len(dic_n)-1]['end'] = end
                dic_n[len(dic_n)-1]['txt'] = txt_temp
                txt_temp = ''

            # alltxt = alltxt + txt + ' '

        text = ('@@@').join([dic_n[d]['txt'] for d in dic_n])
        res,rlist = fun.trans(text)
        srt_c = self.splittime(dic_n,res.split('@@@'))
        # srt_c = self.splittime(srt_c)
    
        srt = ('\n\n').join(srt_c)

        ui.textEdit_2.setText(srt)

    #格式化时间转小数
    def timeswap(self,time):
        shi,fen,miao = time.split(':')
        miao,hmiao = miao.split(',')
        res = 3600*int(shi)+60*int(fen)+int(miao)+int(hmiao)/1000
        return res
    
    #小数时间转格式化
    def swaptiem(self,time):
        shi = int(time/3600)
        if shi<10:
            shi='0'+str(shi)
        else:
            shi = str(shi)

        fen = int((time-3600*int(shi))/60)
        if fen<10:
            fen='0'+str(fen)
        else:
            fen = str(fen)

        miao = int(time - 3600 * int(shi) - 60 * int(fen))
        if miao < 10:
            miao = '0' + str(miao)
        else:
            miao = str(miao)

        hmiao = str(float('0.' + str(time).split('.')[1])*1000)[:3].replace('.','')
        if int(hmiao) < 100:
            hmiao = '0'+hmiao

        return ('%s:%s:%s,%s') % (shi,fen,miao,hmiao)

    def splittime(self,dic_n,tdict):
        srt_c = []
        for index,r in enumerate(tdict):
                dic_n[index]['chs'] = r
                start,end,txt = dic_n[index]['start'],dic_n[index]['end'],dic_n[index]['chs']
                length = len(r)
                if length > 30:
                    i = int(length*19/32)
                    flag = 0  #未添加信号量
                    while i > length*11/32:
                        if r[i] == '，':
                            flag = 1
                            txt1=txt[:i]
                            txt2=txt[i+1:]
                            
                            #计算总时长 按切割比例分时间
                            time_total = self.timeswap(end) - self.timeswap(start)
                            end_num = self.timeswap(start) + time_total*(i/length+0.05)
                            end_n = self.swaptiem(end_num-0.01)
                            start_n = self.swaptiem(end_num + 0.02)
                            
                            srt_c.append('%d\n%s --> %s\n%s' % (len(srt_c) + 1, start, end_n, txt1))
                            srt_c.append('%d\n%s --> %s\n%s' % (len(srt_c) + 1, start_n, end, txt2))
                        i-=1  
                    if flag == 0:
                        srt_c.append('%d\n%s --> %s\n%s'%(len(srt_c)+1,start,end,txt))         
                else:
                    srt_c.append('%d\n%s --> %s\n%s'%(len(srt_c)+1,start,end,txt))
        return srt_c


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Translate()
    ui = Ui_MainWindow()
    ui.setupUi(widget)
    widget.show()

    sys.exit(app.exec_())