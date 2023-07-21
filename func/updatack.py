import sqldata


class write_poeck():

    def __init__(self,ck):
        self.dbdata = sqldata.SqlData("poedata.db")
        self.dbdata.create_table("ckdata")  # 创建表
        self.ck=ck

    def insertdata(self):
        for i in range(0, len(self.ck)):
            try :
                self.dbdata.insertdata("ckdata",self.ck[i],0)  # 插入数据
            except:
                print("请检查ck是否正确")
    def liveck(self):
        data = self.dbdata.readdate("ckdata")
        count_live = 0
        for ck in data:
            if ck[2] == 0:
                count_live += 1
        print("当前可用ck数量为:",count_live+4)
        return count_live
    def run(self):
        self.insertdata()
        self.liveck()
        #data=dbdata.readdate("ckdata")
        #print(data)
        self.dbdata.closedb()



ck=["ck1","ck2","ck3","ck4"]
data=write_poeck(ck)
data.run()





