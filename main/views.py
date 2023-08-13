from django.shortcuts import render ,redirect 
from django.http import HttpResponse
from main.models import Setting,User_data,Ranking
def index(request):
    
    #オープンになっている順位付けがあるか確認
    if Setting.objects.filter(is_open=True).exists():
        hoge=None
        #オープンが2個以上になっていないか確認
        if Setting.objects.filter(is_open=True).count()>1:
            error=1
        #人数設定ミス確認
        elif Setting.objects.get(is_open=True).Num_of_people-User_data.objects.count()!=0:
            hoge=None
            error=3

        else:
            hoge=Setting.objects.get(is_open=True)
            error=0
        
        
    #オープンになっている順位付けがない場合
    else:
        hoge=None
        error=2
    contexts={
        "data":hoge,
        "error":error,
    }
    return render(request,"main/index.html",contexts)

def ranking_progress(request):
    contexts={}
    error=0
    title=""
    if Setting.objects.filter(is_open=True).count()<1 or Setting.objects.filter(is_open=True).count()>1:
        error=1
    elif Setting.objects.filter(is_open=True).count()==1:
        if Setting.objects.get(is_open=True).Num_of_people-User_data.objects.count()!=0:
            error=3
            
        else:
            #順位付け登録状況確認
            list_user=[]
            assintment= Ranking.objects.filter(posted_by=request.user.username,Ranking_title=Setting.objects.get(is_open=True)).values()
            #逆検索的な。
            for y in  User_data.objects.all():
                    list_user.append(y.name)

            for x in assintment:
                if x["name_id"] in list_user:
                    list_user.remove(x["name_id"])
            title=Setting.objects.get(is_open=True)
            contexts["users"]=list_user



    
    contexts["error"]=error
    contexts["title"]=title
    return render(request,"main/progress.html",contexts)

def regist(request):
    #初期化
    
    list_score=[]
    contexts={}
    contexts["error"]=0
    list_rank=[]   

    #method判定
    if request.method == "POST":
        for x in range(Setting.objects.get(is_open=True).Num_of_people,0,-1):
            list_score.append(x)
        score=list_score[int(request.POST["ranking"])-1]
        Ranking_title=Setting.objects.get(Ranking_title=request.POST["Ranking_title"])
        name=User_data.objects.get(name=request.POST["name"])
        z=Ranking(posted_by=request.POST["posted_by"],name=name,ranking=request.POST["ranking"],want_to=request.POST["want_to"],Ranking_title=Ranking_title,score=score,reason=request.POST["reason"])
        z.save()


        list_user=[]
        assintment= Ranking.objects.filter(posted_by=request.user.username,Ranking_title=Setting.objects.get(is_open=True)).values()


        for y in  User_data.objects.all():
                list_user.append(y.name)


        for x in assintment:
            if x["name_id"] in list_user:
                list_user.remove(x["name_id"])


        contexts={
            "data":z,
            "info":"回答を保存しました。",
            "users":list_user,
            "title":Ranking_title
        }
        return render(request,"main/progress.html",contexts)

    if Setting.objects.filter(is_open=True).count()>1 or Setting.objects.filter(is_open=True).count()<1:
        contexts["error"]=3
    else:
            
        registed_of_staff=Setting.objects.get(is_open=True).Num_of_people
        Num_of_staff=User_data.objects.count()
        for i in range(1,Num_of_staff+1):
            list_rank.append(i)

        list_name=[]
        
        
        for y in  User_data.objects.all():
                list_name.append(y.name)
        
        for x in Ranking.objects.filter(posted_by=request.user.username,Ranking_title=Setting.objects.get(is_open=True)).values():
        
            if x["name_id"] in list_name:
                try:
                    list_name.remove(x["name_id"])
                    list_rank.remove(x["ranking"])
                except ValueError:
                        contexts["error"]=3
        
        title=Setting.objects.get(is_open=True)
        
        #設定と登録人数の差異確認
        if Num_of_staff-registed_of_staff>0 or Num_of_staff-registed_of_staff<0:
                contexts["error"]=3
        
        contexts={
            "ranks":list_rank,
            "users":list_name,
            "Setting":title,

        }



    return render(request,"main/regist.html",contexts)

def settings(request):
    if Setting.objects.filter(is_open=True).exists():
    
        if len(Setting.objects.filter(is_open=True))>1:
            hoge=None
            error=1
        else:
            hoge=Setting.objects.get(is_open=True)
            error=0
    else:
        hoge=None
        error=2
    settings=Setting.objects.all()

    contexts={
            "data":hoge,
            "error":error,
            "settings":settings
    }
    
    return render(request,"main/settings.html",contexts)

def join(request):
    contexts={}
    if Setting.objects.filter(is_open=True).count()<1 or Setting.objects.filter(is_open=True).count()>1:
        contexts["error"]=2
    
    else:
        if Setting.objects.get(is_open=True).calculated==True:
            contexts["error"]=1
        if Setting.objects.get(is_open=True).Num_of_people-User_data.objects.count()!=0:
            contexts["error"]=3

        member=[]

        
        if request.method=="POST":
            if request.POST['staff_code'] != "" and request.POST["name"] !="":
                if User_data.objects.filter(staff_code=request.POST['staff_code']).exists()==True:
                    contexts["messages"]="該当の従業員コードはすでに登録済みです。"
                else:
                    User_data(name=request.POST["name"],staff_code=request.POST["staff_code"],score=0).save()
                    contexts["messages"]="登録は正常に終了しました。以下から引き続き登録が可能です。"
            else:
                contexts["error"]=4

        for x in User_data.objects.all():
            member.append("氏名：  {}  (従業員コード: {})".format(x.name,str(x.staff_code)))
        contexts["members"]=member
    return render(request,"main/join.html",contexts)





def set_table(request):
    contexts={}
    if request.method == "POST":
        if request.POST["is_open"] =="0":
            is_open = False
        if request.POST["publicity"] =="0":
            publicity = False
        
        if request.POST["is_open"] =="1":
            is_open = True
        if request.POST["publicity"] =="1":
            publicity = True
        try:
            f=Setting.objects.get(id=request.POST["id"])
        except Setting.DoesNotExist:
            if request.POST["Ranking_title"]:
                Ranking_title=request.POST["Ranking_title"]
            else:
                Ranking_title="未設定"
            if request.POST["Num_of_people"]:
                Num_of_people=request.POST["Num_of_people"]
            else:
                Num_of_people=0
            f=Setting.objects.create(id=request.POST["id"],Ranking_title=Ranking_title,Num_of_people=Num_of_people,is_open=is_open,publicity=publicity)
        if request.POST["Ranking_title"]:
            f.Ranking_title=request.POST["Ranking_title"]
        if request.POST["Num_of_people"] :
            f.Num_of_people=request.POST["Num_of_people"]
        f.publicity=publicity
        f.is_open=is_open
        f.save()
        User_data.objects.update(score=0)
        Setting.objects.filter(is_open=True).update(calculated=False)
    if Setting.objects.count() > 0:
        settings=Setting.objects.all()
        contexts["settings"]=settings
        contexts["id"]=Setting.objects.order_by("id").last().id+1
    else:
        contexts={
            "error":1,
            "id":1
        }

    return render(request,"main/set_table.html",contexts)

def inquiry(request):
    
    contexts={}
    
    if Setting.objects.filter(is_open=True).count()<1 or Setting.objects.filter(is_open=True).count()>1:
        error=3
        
    else:
        yet_list=[]
        if Setting.objects.filter(is_open=True).exists():
            if len(Setting.objects.filter(is_open=True))>1:
                hoge=None
                error=1
            elif Setting.objects.get(is_open=True).Num_of_people-User_data.objects.count()!=0:
                hoge=None
                error=4
            else:
                hoge=Setting.objects.get(is_open=True)
                error=0

        else:
            hoge=None
            error=2
        contexts["data"]=hoge

        for x in User_data.objects.all():
            done=Ranking.objects.filter(Ranking_title=Setting.objects.get(is_open=True),posted_by=x.staff_code).count()
            registed_of_staff=Setting.objects.get(is_open=True).Num_of_people
            if registed_of_staff-done>0:
                yet_list.append(x.name)
        contexts["yet_list"]=yet_list


    contexts["error"]=error

    return render(request,"main/inquiry.html",contexts)

def results(request):
    contexts={}
    yet_list=[]
    can_show=False
    result_total=[]
    result_other=[]
    #設定ミス判定開始
    if Setting.objects.filter(is_open=True).count()!=1:
        error=3
    elif Setting.objects.filter(is_open=True).exists():
        
        if len(Setting.objects.filter(is_open=True))>1:
            hoge=None
            error=1
        elif Ranking.objects.all().count() > (User_data.objects.all().count())**2:
            hoge = None
            error = 4
            
        else:
            hoge=Setting.objects.get(is_open=True)
            error=0
            for x in User_data.objects.all():
                done=Ranking.objects.filter(Ranking_title=Setting.objects.get(is_open=True),posted_by=x.staff_code).count()
                registed_of_staff=Setting.objects.get(is_open=True).Num_of_people
                if registed_of_staff-done>0:
                    yet_list.append(x.name)
            if len(yet_list)==0 and Setting.objects.filter(is_open=True).count()==1 and Setting.objects.get(is_open=True).calculated==True:
                can_show=True
            contexts["data"]=hoge

    else:
        hoge=None
        error=2
        contexts["data"]=hoge
    
    

    if can_show==True:

    #設定ミス判定終了
        users=[]
        staff_codes=[]
        ranking=[]
        point=[]
        reason=[]
        want_to=[]
        posted_by=[]
        names=[]
        rank=[]
        #対象者情報抽出
        for y in range(1,User_data.objects.count()+1):
            ranking.append(y)
        
        #総合順位・ポイント用データ抽出
        for x in User_data.objects.order_by("-score"):
            users.append(x.name)
            staff_codes.append(x.staff_code)
            point.append(x.score)

        #理由・こうしたら良くなるデータ抽出
        for a in User_data.objects.all():
            name=a.name
            #名前順にまとめて先頭からデータを1つのリストに格納
            for x in Ranking.objects.filter(Ranking_title=Setting.objects.get(is_open=True),name=name).order_by("-score"):
                reason.append(x.reason)
                want_to.append(x.want_to)
                user_name=User_data.objects.get(staff_code=x.posted_by)
                posted_by.append(str(user_name))
                names.append(str(x.name))
                rank.append(x.ranking)

        

    #総合順位・ポイント用データ整形
        for x in range(User_data.objects.count()):
            z=[]
            z.append(ranking[x])
            z.append(users[x])
            z.append(staff_codes[x])
            z.append(point[x])    
            result_total.append(z)
        
        #理由・こうしたら良くなる用データ整形
        for i in range(User_data.objects.count()**2):
            z=[]
            z.append(names[i])
            z.append(rank[i])
            z.append(reason[i])
            z.append(want_to[i])
            if Setting.objects.get(is_open=True).publicity ==True:
                z.append(posted_by[i])
            result_other.append(z)




    contexts["can_show"]=can_show
    contexts["error"]=error
    contexts["result_total"]=result_total
    contexts["result_other"]=result_other

    return render(request,"main/results.html",contexts)


def calculate(request):
    contexts={}
    yet_list=[]
    end=0
    can_show=False
    #設定ミス確認(受付中の順位付け)
    if Setting.objects.filter(is_open=True).exists():
        if len(Setting.objects.filter(is_open=True))>1:
            hoge=None
            error=1
        else:
            hoge=Setting.objects.get(is_open=True)
            error=0
    else:
        hoge=None
        error=2
    if Setting.objects.filter(is_open=True).count()<1 or Setting.objects.filter(is_open=True).count()>1:
        error=4
    else:
            #投票人数確認・設定ミス確認
        for x in User_data.objects.all():
            done=Ranking.objects.filter(Ranking_title=Setting.objects.get(is_open=True),posted_by=x.staff_code).count()
            registed_of_staff=Setting.objects.get(is_open=True).Num_of_people
            if registed_of_staff-done>0:
                yet_list.append(x.name)
        if len(yet_list)!=0 and Setting.objects.filter(is_open=True).count()==1:
            error=3
        if Setting.objects.get(is_open=True).calculated==True:
            error=6
        if Setting.objects.get(is_open=True).Num_of_people-User_data.objects.count()!=0:
            error=8
        if request.method =="POST":
            #集計開始
            if request.POST["calculate"]=="on":
                if len(yet_list)==0 and Setting.objects.filter(is_open=True).count()==1:
                    can_show=True
                    for x in User_data.objects.all():
                        result_score=0
                        name=str(x.name)
                        for y in Ranking.objects.filter(Ranking_title=Setting.objects.get(is_open=True),name=name):
                            result_score+=y.score
                        z=User_data.objects.filter(name=name).get()
                        z.score=result_score
                        z.save()
                n=Setting.objects.get(is_open=True)
                n.calculated=True
                n.save()
                error=7
            #集計終了
                
            else:
                error=5


    contexts["end"]=end
    contexts["can_show"]=can_show
    contexts["error"]=error
    contexts["data"]=hoge


    return render(request,"main/calculate.html",contexts)


