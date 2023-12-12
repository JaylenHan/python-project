import tkinter, time, random , pygame
from tkinter import messagebox

key=""
mouseX,mouseY,mouseC=0,0,0
story_index=0
chr_num=0  # 캐릭터 선택 변수 (승헌=0 / 지민=1 / 민서=2 / 병찬=3)
mx,my=6,6
current_map="home"
map_num,boss_num,catch_boss=0,0,0
damage=0
hp,mp,energy,coin=0,0,0,0
items=["mp","energy","hp"]
esc_try=0

class GameCharacter:
    def __init__(self,name,life,power,gauge,imgfile,tagname,x,y,di):
        self.name=name
        self.lmax=life
        self.life=life
        self.power=power
        self.lpower=power
        self.gauge=gauge
        self.imgfile=tkinter.PhotoImage(file=imgfile)
        self.tagname=tagname
        self.x=x
        self.y=y
        self.di=di #플레이어(왼쪽)=1 / 몬스터(오른쪽)=-1
    def chat_draw(self):       # 대화 화면 생성
        if self.di==1:
            canvas.create_image(self.x+100,self.y-120,image=self.imgfile,tag=self.tagname)
        else:
            canvas.create_image(self.x-150,self.y+150,image=self.imgfile,tag=self.tagname)

    def chat_remove(self):     # 대화 화면 제거
        self.chat_draw()
        canvas.delete("chat_screen")
        canvas.delete(self.tagname)

    def draw_player(self):     # 플레이어 캐릭터 UI
        if canvas.find_withtag("BATTLE"):
            canvas.create_image(self.x,self.y,image=self.imgfile,tag=self.tagname) #전투 캐릭터 출력
            canvas.create_text(480,480,text=self.name,tag=self.tagname,font=("휴먼매직체",30)) #이름출력
            canvas.create_rectangle(400,508,800,558,fill="white",outline="black",width=5) #HP테두리 출력
            canvas.create_text(650,480,text="HP ",font=("휴먼매직체",25,"bold"),anchor="e",tag=self.tagname)
            canvas.create_text(650,480,text="{} / {}".format(self.life,self.lmax),font=("휴먼매직체",25),anchor="w",tag=self.tagname)
            for i in range(self.life-damage):
                canvas.create_rectangle(400+i*(400/self.lmax),508,400+(i+1)*(400/self.lmax),558,fill="green",tag=self.tagname,width=0)

            for i in range(4): #게이지 출력
                canvas.create_rectangle(400+i*100,568,400+(i+1)*100,568+50,fill="white",outline="black",width=5)
            for i in range(self.gauge):
                canvas.create_rectangle(400+i*100,568,400+(i+1)*100,568+50,fill="skyblue",tag=self.tagname)

    def draw_boss(self):       # 몬스터 UI
        if canvas.find_withtag("BATTLE"):
            canvas.create_image(self.x-20,self.y,image=self.imgfile,tag=self.tagname)
            canvas.create_text(1130,85,text=self.name,tag=self.tagname,font=("휴먼매직체",30))
            canvas.create_rectangle(780,108,1180,158,fill="white",outline="black",width=5)
            canvas.create_text(830,85,text="HP ",font=("휴먼매직체",25,"bold"),anchor="e",tag=self.tagname)
            canvas.create_text(830,85,text="{} / {}".format(self.life,self.lmax),font=("휴먼매직체",25),anchor="w",tag=self.tagname)
            for i in range(self.life-damage):
                canvas.create_rectangle(780+i*(400/self.lmax),108,780+(i+1)*(400/self.lmax),158,fill="green",tag=self.tagname,width=0)
    
    def attack_motion(self):   # 공격 모션 (플레이어 + 보스 몹)
        if canvas.find_withtag("BATTLE"):
            if self.di==1:
                for i in range(5):
                    canvas.coords(self.tagname,self.x+i*15,self.y-i*15)
                    canvas.update()
                    time.sleep(0.09)
                canvas.coords(self.tagname,self.x,self.y)
            elif self.di==-1:
                canvas.delete(chr_boss[boss_num].tagname)
                chr_boss[boss_num].imgfile=boss_chr[boss_num][1] # 보스 스킬 모션으로 이미지 변경
                chr_boss[boss_num].draw_boss()
                canvas.update()
                time.sleep(0.6)
                canvas.delete(chr_boss[boss_num].tagname)
                canvas.update()
                chr_boss[boss_num].imgfile=boss_chr[boss_num][0] # 보스 대기 모션으로 이미지 변경
                chr_boss[boss_num].draw_boss()
                canvas.update()

    def player_damaged(self):  # 플레이어 피격 시
        if canvas.find_withtag("BATTLE"):
            for i in range(5):
                self.draw_player()
                canvas.update()
                time.sleep(0.09)
                canvas.delete(self.tagname)
                canvas.update()
                time.sleep(0.09)
            if boss_num==0:                    # 보스 별 공격력 상이
                damage=random.randint(10,15)
            elif boss_num==1:
                damage=random.randint(15,20)
            elif boss_num==2:
                damage=random.randint(20,30)
            self.life=self.life-damage
            if self.life<=0:
                self.life=0
            if self.life>0:
                self.draw_player()
            else:
                canvas.delete(character[chr_num].tagname)
                character[chr_num].imgfile=chr_dead
                character[chr_num].draw_player()
                canvas.update()
                time.sleep(1.2)
                character[chr_num].imgfile=chr_battle[chr_num]

    def boss_damaged(self):
        for i in range(5):
            canvas.delete(self.tagname)
            self.draw_boss()
            canvas.update()
            time.sleep(0.09)
            canvas.delete(self.tagname)
            canvas.update()
            time.sleep(0.09)
        if self.life>0:
            self.draw_boss()
        else:
            canvas.delete(chr_boss[boss_num].tagname)
            chr_boss[boss_num].imgfile=chr_dead
            chr_boss[boss_num].draw_boss()
            canvas.update()
            time.sleep(1.2)
            chr_boss[boss_num].imgfile=boss_chr[boss_num][0]

    def scratch_attack(self):    # 플레이어 기본공격  (난수 0.8이상이면 데미지x2)
        if canvas.find_withtag("BATTLE"):
            x=random.random()
            if x>=0.8:
                x=2
                canvas.create_text(353,303,text="x2 Critical !",font=("휴먼매직체",70),fill="black",tag="TEXT")
                canvas.create_text(350,300,text="x2 Critical !",font=("휴먼매직체",70),fill="red",tag="TEXT")
                canvas.after(1000,delete_text)
            else:
                x=1
            canvas.create_image(800,448,image=atk_scratch,tag="SKILL")
            canvas.update()
            time.sleep(0.6)
            canvas.delete("SKILL")
            canvas.update()
            self.life=self.life-character[chr_num].power*x
            if self.life<=0:
                self.life=0
            self.boss_damaged()

    def bite_attack(self):    # 플레이어 기본공격  (난수 0.8이상이면 데미지x2)
        if canvas.find_withtag("BATTLE"):
            x=random.random()
            if x>=0.8:
                x=2
                canvas.create_text(353,303,text="x2 Critical !",font=("휴먼매직체",70),fill="black",tag="TEXT")
                canvas.create_text(350,300,text="x2 Critical !",font=("휴먼매직체",70),fill="red",tag="TEXT")
                canvas.after(1000,delete_text)
            else:
                x=1
            canvas.create_image(800,448,image=atk_bite,tag="SKILL")
            canvas.update()
            time.sleep(0.6)
            canvas.delete("SKILL")
            canvas.update()
            self.life=self.life-character[chr_num].power*x
            if self.life<=0:
                self.life=0
            self.boss_damaged()
    
    def special_attack(self):  # 플레이어 스킬 공격
        if canvas.find_withtag("BATTLE"):
            x=random.choice([2,3,3,3,4,4,4,4,5,5])
            if x==3:
                canvas.create_text(353,303,text="x3 Critical !",font=("휴먼매직체",70),fill="black",tag="TEXT")
                canvas.create_text(350,300,text="x3 Critical !",font=("휴먼매직체",70),fill="mediumpurple",tag="TEXT")
                canvas.update()
                canvas.after(1500,delete_text)
            elif x==4:
                canvas.create_text(353,303,text="x4 Critical !!",font=("휴먼매직체",75),fill="black",tag="TEXT")
                canvas.create_text(350,300,text="x4 Critical !!",font=("휴먼매직체",75),fill="red",tag="TEXT")
                canvas.update()
                canvas.after(1500,delete_text)
            elif x==5:
                canvas.create_text(353,303,text="x5 Critical !!",font=("휴먼매직체",80),fill="black",tag="TEXT")
                canvas.create_text(350,300,text="x5 Critical !!",font=("휴먼매직체",80),fill="yellow",tag="TEXT")
                canvas.update()
                canvas.after(1500,delete_text)
            canvas.delete(character[chr_num].tagname)          # 캐릭터 스킬 모션 취함
            character[chr_num].imgfile=chr_skill[chr_num]
            character[chr_num].draw_player()
            canvas.create_image(800,448,image=skill_motion[chr_num],tag="SKILL")
            canvas.update()
            time.sleep(0.6)
            canvas.delete(character[chr_num].tagname)
            canvas.delete("SKILL")
            character[chr_num].imgfile=chr_battle[chr_num]
            character[chr_num].draw_player()
            canvas.update()
            self.life=self.life-character[chr_num].power*x
            if self.life<=0:
                self.life=0
            self.boss_damaged()

    def remove_player(self):
        self.draw_player()
        canvas.delete(self.tagname)

class Targetgame:   # 민서 게임
    def __init__(self, root):
        self.root = root
        self.root.title("과녁 맞히기")
        self.tmr = 3  # 시간 카운트 변수
        self.target_cnt = 0  # 표적 카운트 변수
        self.coin_cnt = 0  # 코인 카운트 변수
        self.play_time = 30  # 플탐 변수
        self.game_running = False  # 게임이 진행 중인지 여부를 나타내는 변수 추가

        # 이미지 변수 & 이미지 가로/세로 변수
        self.target_img = tkinter.PhotoImage(file="target.png")
        self.coin_img = tkinter.PhotoImage(file="coin.png")
        self.cursor_img = tkinter.PhotoImage(file="aim_cursor.png")
        self.start_img = tkinter.PhotoImage(file="start_bg.png")
        self.howto_img = tkinter.PhotoImage(file="howto_bg.png")
        self.game_img = tkinter.PhotoImage(file="game_bg.png")
        self.end_img = tkinter.PhotoImage(file="end_bg.png")
        self.target_width = self.target_img.width()
        self.target_height = self.target_img.height()
        self.coin_width = self.coin_img.width()
        self.coin_height = self.coin_img.height()
        self.cursor_width = self.cursor_img.width()
        self.cursor_height = self.cursor_img.height()

        # 플레이 중 UI
        self.UI = tkinter.Frame(root)  # UI 배치할 프레임 생성
        self.UI.pack_forget()
        self.target_label = tkinter.Label(self.UI, text="표적: 0", font=("나무", 20, "bold"), fg="black")  # 표적UI (in 프레임)
        self.target_label.pack(side=tkinter.LEFT, padx=20)
        self.coin_label = tkinter.Label(self.UI, text="코인: 0", font=("나무", 20, "bold"), fg="black")  # 코인UI (in 프레임)
        self.coin_label.pack(side=tkinter.LEFT, padx=20)
        self.time_label = tkinter.Label(self.UI, text=f"남은 시간: 00:{self.play_time:02d}", font=("나무", 20, "bold"), fg="black")
        self.time_label.pack(side=tkinter.LEFT, padx=20)

        # 타겟 위치 관리 리스트
        self.target_generate = []
        self.coin_generate = []

        # 시작 화면 캔버스
        self.start_pg = tkinter.Canvas(root, width=1600, height=896)
        self.start_bg = self.start_pg.create_image(800, 448, image=self.start_img)
        self.start_pg.pack()
        start_btn = tkinter.Button(self.start_pg, text="플레이", font=("나무", 36, "bold"), padx=100, command=self.after_start_btn)  # 플레이 버튼
        start_btn.place(x=608, y=520)
        howto_btn = tkinter.Button(self.start_pg, text="설명", font=("나무", 36, "bold"), padx=124, command=self.after_howto_btn)  # 게임설명 버튼
        howto_btn.place(x=608, y=650)
        end_btn=tkinter.Button(self.start_pg, text="종료", font=("나무", 36, "bold"), padx=124, command=self.after_end_btn)
        end_btn.place(x=608,y=780)
        # 설명 화면 캔버스
        self.howto_pg = tkinter.Canvas(root, width=1600, height=896)
        self.howto_bg = self.howto_pg.create_image(800, 448, image=self.howto_img)
        self.howto_pg.pack_forget()
        return_btn = tkinter.Button(self.howto_pg, text="플레이", font=("나무", 36, "bold"), padx=100, command=self.after_start_btn)  # 설명화면 플레이 버튼
        return_btn.place(x=628, y=700)
        # 플레이 화면 캔버스
        self.game_pg = tkinter.Canvas(root, width=1600, height=896)
        self.game_bg = self.game_pg.create_image(800, 448, image=self.game_img)
        self.game_pg.pack_forget()
        # 결과 화면 캔버스
        self.end_pg = tkinter.Canvas(root, width=1600, height=896)
        self.end_bg = self.end_pg.create_image(800, 448, image=self.end_img)
        self.end_pg.pack_forget()
        retry_btn = tkinter.Button(self.end_pg, text="종료", font=("나무", 24, "bold"), padx=50, command=self.after_end_btn)  # 게임종료 버튼
        retry_btn.place(x=1300, y=800)

        # 커서 설정
        self.cursor = self.game_pg.create_image(800, 448, image=self.cursor_img)
        self.game_pg.bind("<Motion>", self.move_aim)

    def after_howto_btn(self):  # 설명 화면 ('설명'버튼을 누른 후)
        self.start_pg.pack_forget()
        self.howto_pg.pack()

    def after_start_btn(self):  # 플레이 화면 ('플레이'버튼을 누른 후)
        self.start_pg.pack_forget()
        self.howto_pg.pack_forget()
        root.config(cursor="none")  # 커서 숨김
        self.game_pg.pack()
        self.UI.pack()
        self.play_game()

    def after_end_btn(self):
        self.root.destroy()
        close_toplevel()

    def st_cnt_dwn(self, cnt):  # 플레이 전 3초 카운트 다운
        if self.tmr >= 0:
            cnt["text"] = self.tmr if self.tmr > 0 else "Start!"
            self.tmr -= 1
            self.root.after(1000, self.st_cnt_dwn, cnt)
        elif self.tmr < 0:
            cnt.destroy()
            self.game_running = True  # 게임이 시작되었음을 나타내는 플래그 설정
            self.start_time = time.time()  # 시작 시간 기록
            self.start_animation()

    def start_animation(self): # 게임 중 애니메이션
        if not self.game_running: # 게임 끝나면 함수 스킵
            return
        cur_time = time.time()
        el_time = cur_time - self.start_time
        if el_time < self.play_time:
            self.create_target()
            self.create_coin()
            self.root.after(2000, self.remove_target)  # 표적 유지 시간
            self.root.after(1000, self.remove_coin)  # 코인 유지 시간 (0.5초)
            self.root.after(500, self.update_time)  # 0.5초 후 남은 시간 업데이트
            self.root.after(500, self.start_animation)  # 0.5초 후 함수 재시작

    def create_target(self): # 표적 생성 (화면 속 최대 8개)
        num_targets = random.randint(1,4)  # 한번에 1~4개 생성
        for _ in range(num_targets):
            if len(self.target_generate) < 8:
                image = self.target_img
                x = random.randint(0, 1600 - self.target_width) # 화면 이탈 방지
                y = random.randint(0, 896 - self.target_height)
                image_instance = self.game_pg.create_image(x, y, anchor=tkinter.NW, image=image)
                self.target_generate.append(image_instance)
                self.game_pg.tag_bind(image_instance, '<Button-1>', lambda void, inst=image_instance: self.image_clicked(inst, 'target')) # 이미지 클릭 이벤트

    def create_coin(self): # 코인 생성 (화면 속 최대 1개)
        if len(self.coin_generate) < 1:
            image = self.coin_img
            x = random.randint(0, 1600 - self.coin_width) # 화면 이탈 방지
            y = random.randint(0, 896 - self.coin_height)
            image_instance = self.game_pg.create_image(x, y, anchor=tkinter.NW, image=image)
            self.coin_generate.append(image_instance)
            self.game_pg.tag_bind(image_instance, '<Button-1>', lambda void, inst=image_instance: self.image_clicked(inst, 'coin')) # 이미지 클릭 이벤트

    def remove_target(self): # 표적 삭제
        if self.target_generate:
            image_instance = self.target_generate.pop(0)
            self.game_pg.delete(image_instance)

    def remove_coin(self): # 코인 삭제
        if self.coin_generate:
            image_instance = self.coin_generate.pop(0)
            self.game_pg.delete(image_instance)

    def image_clicked(self, instance, image_type): # 목표물 클릭 시
        if self.game_running:  # 게임 중일 때만 클릭 반응 (3초 카운트 다운 이후)
            if image_type == 'target':
                self.target_cnt += 1
                self.target_label.config(text=f"표적: {self.target_cnt}")
            elif image_type == 'coin':
                self.coin_cnt += 1
                self.coin_label.config(text=f"코인: {self.coin_cnt}")
            self.game_pg.delete(instance) # 즉시 이미지 삭제

    def update_time(self): # 남은 시간 표시
        cur_time = time.time()
        el_time = cur_time - self.start_time
        remaining_time = max(0, self.play_time - el_time)
        seconds = int(remaining_time)
        time_str = f"남은 시간: 00:{seconds:02d}"
        self.time_label.config(text=time_str)

    def move_aim(self, e): # 에임 이미지 커서 따라가기
        self.game_pg.coords(self.cursor, e.x - self.cursor_width // 10, e.y - self.cursor_height // 10)

    def end_game(self): # 게임 종료
        global coin
        self.game_running = False  # 게임 종료 플래그
        self.game_pg.pack_forget()
        self.UI.pack_forget()
        self.end_pg.pack()
        self.root.config(cursor="") # 커서 보이기
        self.final_coin = self.target_cnt // 10 + self.coin_cnt # 해당 판 총 획득 코인 수 (main 코드와 연결할 때 소지 중인 코인에 합하는 변수)
        texts = [("맞힌 표적 수", self.target_cnt, 325), ("맞힌 코인 수", self.coin_cnt, 425), ("획득 코인 수", self.final_coin, 630)]
        for text, value, y in texts:
            result_text = tkinter.Text(self.end_pg, font=("나무", 40, "bold"), height=1, width=16)
            result_text.insert(tkinter.END, f"{text}: {value}개")
            result_text.place(x=580, y=y)
        
        coin+=self.final_coin
        coin_label.config(text=f"x {coin}")

    def play_game(self): # 게임 시작
        self.cnt_dwn = tkinter.Label(self.root,font=("Arial", 200), padx=30)
        self.cnt_dwn.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.st_cnt_dwn(self.cnt_dwn)
        self.root.after(34000, self.end_game)

class PackMan:      # 승헌 게임
    def __init__(self, master):
        self.master = master
        self.master.title("팩맨")
        self.direction = "Right"
        self.item = None
        self.score, self.coins = 0, 0
        self.pacman_speed = 60
        self.ghost_speed = 60
        self.item_speed = 60
        self.game_running = False
        self.play_time = 30 # 플탐 변수

        # 게임 중 UI
        self.UI = tkinter.Frame(master)
        self.UI.pack_forget()
        self.score_label = tkinter.Label(self.UI, text="점수 : 0", font=("나무", 20, "bold"), fg="black")
        self.score_label.pack(side=tkinter.LEFT, padx=20)
        self.coin_label = tkinter.Label(self.UI, text="코인 : 0", font=("나무", 20, "bold"), fg="black")
        self.coin_label.pack(side=tkinter.LEFT, padx=20)
        self.time_label = tkinter.Label(self.UI, text=f"남은 시간: 00:{self.play_time:02d}", font=("나무", 20, "bold"), fg="black")
        self.time_label.pack(side=tkinter.LEFT, padx=20)
        # 시작화면 캔버스
        self.start_pg = tkinter.Canvas(master, bg="black", width=1200, height=960)
        self.start_pg.pack()
        self.start_pg.create_arc(250, 60, 950, 760,start=30, extent=300, fill="pink", outline="black",width=8,tag="title")
        self.start_pg.create_text(602,302,text="   King-Man\n      Game",font=("나무", 55, "bold"),fill="purple",tag="title")
        self.start_pg.create_text(600,300,text="   King-Man\n      Game",font=("나무", 55, "bold"),fill="yellow",tag="title")
        start_btn = tkinter.Button(self.start_pg, text="플레이", font=("나무", 36, "bold"), width=8, command=self.after_start_btn)
        start_btn.place(x=500, y=680)
        end_btn = tkinter.Button(self.start_pg, text="종 료", font=("나무", 36, "bold"), width=8, command=self.after_end_btn)
        end_btn.place(x=500, y=810)
        # 플레이화면 캔버스
        self.game_pg = tkinter.Canvas(master, bg="black", width=1200, height=960)
        self.pacman = self.game_pg.create_arc(0, 0, 60, 60,start=30, extent=300, fill="pink", outline="black")
        self.ghost1 = self.game_pg.create_rectangle(20 * 60 - 60 , 15 * 60 - 60 , 20 * 60 , 15 * 60, fill="red")
        self.ghost2 = self.game_pg.create_rectangle(0, 15 * 60 - 60, 60, 15 * 60, fill="red")
        self.ghost3 = self.game_pg.create_rectangle(20 * 60 - 60, 0,20 * 60, 60, fill="red")
        self.game_pg.pack_forget()
        self.game_pg.focus_set()
        self.game_pg.bind("<KeyPress>", self.on_key_press)
        #결과 화면 캔버스
        self.end_pg = tkinter.Canvas(master, bg="black", width=1200, height=960)
        self.end_pg.pack_forget()
        restart_btn = tkinter.Button(self.end_pg, text="게임종료", font=("나무", 36, "bold"), width=8, command=self.after_end_btn)
        restart_btn.place(x=935, y=850)

    def after_start_btn(self):  # 플레이 버튼 누른 뒤
        self.start_pg.pack_forget()
        self.start_pg.delete("title")
        self.game_pg.pack()
        self.UI.pack()
        self.play_game()

    def after_end_btn(self):  # 종료 버튼 누른 뒤 
        self.master.destroy()
        close_toplevel()
   
    def on_key_press(self, event):  # 방향키 감지
        key = event.keysym
        if key in ["Up", "Down", "Left", "Right"]:
            self.direction = key
            self.update_pacman_mouth()

    def update(self): # 업데이트
        if self.game_running:
            self.move_pacman()
            self.move_ghost(self.ghost1)
            self.move_ghost(self.ghost2)
            self.move_ghost(self.ghost3)
            self.check_item_collision()
            self.check_game_over()
            self.update_time()
        self.game_pg.after(100, self.update)

    def move_pacman(self):
        x, y, _, _ = self.game_pg.coords(self.pacman)
        if self.direction == "Up" and y > 0:
            self.game_pg.move(self.pacman, 0, -self.pacman_speed)
        elif self.direction == "Down" and y < 15 * 60 - 60 // 2:
            self.game_pg.move(self.pacman, 0, self.pacman_speed)
        elif self.direction == "Left" and x > 0:
            self.game_pg.move(self.pacman, -self.pacman_speed, 0)
        elif self.direction == "Right" and x < 20 * 60 - 60:
            self.game_pg.move(self.pacman, self.pacman_speed, 0)
        self.update_pacman_mouth()

    def move_ghost(self, ghost):
        if self.game_running:
            x, y, _, _ = self.game_pg.coords(ghost)
            rand_direction = random.choice(["Up", "Down", "Left", "Right"])
            if rand_direction == "Up" and y > 0:
                self.game_pg.move(ghost, 0, -self.ghost_speed)
            elif rand_direction == "Down" and y < 15 * 60 - 60:
                self.game_pg.move(ghost, 0, self.ghost_speed)
            elif rand_direction == "Left" and x > 0:
                self.game_pg.move(ghost, -self.ghost_speed, 0)
            elif rand_direction == "Right" and x < 20 * 60 - 60:
                self.game_pg.move(ghost, self.ghost_speed, 0)

    def update_pacman_mouth(self):
        angle = {"Up": 90, "Down": 270, "Left": 180, "Right": 0}
        self.game_pg.itemconfig(self.pacman, start=30 + angle[self.direction], extent=350 - 2 * 30)

    def create_item(self):
        x = random.randint(0, 20 - 1) * 60
        y = random.randint(0, 15 - 1) * 60
        self.item = self.game_pg.create_oval(x, y, x + 60, y + 60, fill="blue", tag="ITEM")

    def check_item_collision(self):
        if self.item:
            pacman_coords = self.game_pg.coords(self.pacman)
            item_coords = self.game_pg.coords(self.item)
            if item_coords:
                if (
                    pacman_coords[0] < item_coords[2]
                    and pacman_coords[2] > item_coords[0]
                    and pacman_coords[1] < item_coords[3]
                    and pacman_coords[3] > item_coords[1]
                ):
                    self.score += 1
                    self.coins += 2
                    self.score_label.config(text=f"점수: {self.score}")
                    self.coin_label.config(text=f"코인: {self.coins}")
                    self.game_pg.delete(self.item)
                    self.create_item()

    def update_time(self):
        cur_time = time.time()
        el_time = cur_time - self.start_time
        remaining_time = max(0, self.play_time - el_time)
        seconds = int(remaining_time)
        time_str = f"남은 시간: 00:{seconds:02d}"
        self.time_label.config(text=time_str)

    def check_game_over(self):
        pacman_coords = self.game_pg.coords(self.pacman)
        ghost_coords1 = self.game_pg.coords(self.ghost1)
        ghost_coords2 = self.game_pg.coords(self.ghost2)
        ghost_coords3 = self.game_pg.coords(self.ghost3)

        if (self.check_collision(pacman_coords, ghost_coords1) or self.check_collision(pacman_coords, ghost_coords2) or self.check_collision(pacman_coords, ghost_coords3) or self.check_time_limit_exceeded()):
            self.end_game()
            self.game_running = True
            self.pacman_speed = 0
            self.ghost_speed = 0
            self.item_speed = 0

    def check_collision(self, coords1, coords2):
        return (coords1[0] < coords2[2] and coords1[2] > coords2[0]
            and coords1[1] < coords2[3] and coords1[3] > coords2[1])

    def check_time_limit_exceeded(self):
        elapsed_time = time.time() - self.start_time
        return elapsed_time > self.play_time

    def start_animation(self): # 게임 중 애니메이션
        if not self.game_running: # 게임 끝나면 함수 스킵
            return
        cur_time = time.time()
        el_time = cur_time - self.start_time
        if el_time < self.play_time:
            self.master.after(500, self.update_time)  # 0.5초 후 남은 시간 업데이트
            self.master.after(500, self.start_animation)  # 0.5초 후 함수 재시작

    def end_game(self):
        global coin
        self.game_running = False
        self.game_pg.delete("ITEM")
        self.game_pg.pack_forget()
        self.UI.pack_forget()
        self.end_pg.pack()
        self.result_text = self.end_pg.create_text(20 * 60 // 2, 15 * 60 // 2 + 30,
            text=f"게임 오버\n점수: {self.score}, 코인: {self.coins}",font=("Helvetica", 40,"bold"),fill="white",tag="TEXT")
        self.master.after_cancel(self.update_id)

        coin+=self.coins
        coin_label.config(text=f"x {coin}")
    
    def play_game(self):
        self.game_running=True
        self.start_time=time.time()
        self.create_item()
        self.update_id = self.master.after(100, self.update)
        self.start_animation()
        self.master.after(30000, self.end_game)

class CollegeGame:  # 지민 게임
    def __init__(self, master):
        self.master = master
        self.master.title("대학 학점 먹기 게임")
        self.score = 0
        self.coin=0
        self.game_running = False
        self.play_time = 30
        
        # 학점 이미지들
        self.start_img=tkinter.PhotoImage(file="ddongmap.png")
        self.character_image = tkinter.PhotoImage(file="lamb.png")
        self.grade_images = {
            "A": tkinter.PhotoImage(file="A.png"),
            "B": tkinter.PhotoImage(file="B.png"),
            "C": tkinter.PhotoImage(file="C.png"),
            "D": tkinter.PhotoImage(file="D.png"),
            "F": tkinter.PhotoImage(file="F.png"),
            "F2": tkinter.PhotoImage(file="F.png")}
        
        # 플레이 중 UI
        self.UI=tkinter.Frame(master)
        self.UI.pack_forget()
        self.score_label=tkinter.Label(self.UI,text="점수: 0",font=("나무", 20, "bold"), fg="black")
        self.score_label.pack(side=tkinter.LEFT,padx=20)
        self.coin_label = tkinter.Label(self.UI, text="코인: 0", font=("나무", 20, "bold"), fg="black")  # 코인UI (in 프레임)
        self.coin_label.pack(side=tkinter.LEFT, padx=20)
        self.time_label = tkinter.Label(self.UI, text=f"남은 시간: 00:{self.play_time:02d}", font=("나무", 20, "bold"), fg="black")
        self.time_label.pack(side=tkinter.LEFT, padx=20)

        # 시작화면 캔버스
        self.start_pg = tkinter.Canvas(master, width=1200, height=600, bg="white")
        self.start_bg=self.start_pg.create_image(600,300,image=self.start_img)
        self.start_pg.pack()
        self.start_pg.create_text(602,202,text="  학점따기\n    Game",font=("나무", 55, "bold"),fill="white",tag="title")
        self.start_pg.create_text(600,200,text="  학점따기\n    Game",font=("나무", 55, "bold"),fill="royalblue",tag="title")
        start_btn=tkinter.Button(self.start_pg,text="플레이",font=("나무",36,"bold"),width=8,command=self.after_start_btn)
        start_btn.place(x=486,y=380)
        end_btn=tkinter.Button(self.start_pg,text="종료",font=("나무",36,"bold"),width=8,command=self.after_end_btn)
        end_btn.place(x=486,y=490)

        # 게임화면 캔버스
        self.game_pg=tkinter.Canvas(master,width=1200,height=600)
        self.game_bg=self.game_pg.create_image(600,300,image=self.start_img)
        self.character = self.game_pg.create_image(600, 550, anchor=tkinter.S, image=self.character_image)
        self.game_pg.pack_forget()

        # 결과 화면 캔버스
        self.end_pg = tkinter.Canvas(master, width=1200, height=600)
        self.end_bg = self.end_pg.create_image(600,300, image=self.start_img)
        self.end_pg.pack_forget()
        retry_btn = tkinter.Button(self.end_pg, text="종료", font=("나무", 45, "bold"), padx=50,command=self.after_end_btn)
        retry_btn.place(x=910, y=460)
        self.end_pg.pack_forget()

        # 키 바인딩
        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)

    def after_start_btn(self):
        self.start_pg.pack_forget()
        self.start_pg.delete("title")
        self.game_pg.pack()
        self.UI.pack()
        self.play_game()
        
    def after_end_btn(self):
        self.master.destroy()
        close_toplevel()

    def move_left(self, event): # 왼쪽으로 이동
        if self.game_running and self.character_exists():
            current_x = self.game_pg.coords(self.character)[0]
            if current_x > 20:
                self.game_pg.move(self.character, -20, 0)

    def move_right(self, event): # 오른쪽으로 이동
        if self.game_running and self.character_exists():
            current_x = self.game_pg.coords(self.character)[0]
            if current_x < 1180:
                self.game_pg.move(self.character, 20, 0)

    def character_exists(self): # 캐릭터가 존재하는지 확인
        return self.game_pg.coords(self.character) if self.character else None

    def spawn_grade(self):
        # 학점 생성
        if self.game_running:
            grades = ["A", "B", "C", "D", "F", "F2"]
            random_grade = random.choice(grades)
            x_position = random.randint(50, 1000)

            grade_image = self.grade_images[random_grade]
            grade = self.game_pg.create_image(x_position, 0, anchor=tkinter.N, image=grade_image)

            self.move_grade(grade, random_grade)
            self.master.after(1000, self.spawn_grade)

    def move_grade(self, grade, grade_type):
        if self.game_running and self.game_pg.coords(grade)[1] < 400:
            self.game_pg.move(grade, 0, 10)

        # 캐릭터와의 충돌 확인
            if self.check_collision(grade, self.character):
                self.handle_collision(grade_type)
                self.game_pg.delete(grade)
            self.master.after(100, lambda: self.move_grade(grade, grade_type))
        else:
            if self.game_running:
                self.game_pg.delete(grade)

    def check_collision(self, item1, item2):  
        # 두 항목(학점 및 캐릭터)이 겹치는지 확인
        x1, y1, _, _ = self.game_pg.bbox(item1)
        x2, y2, _, _ = self.game_pg.bbox(item2)
        char_bounding_box_size = 30
        grade_bounding_box_size = 30
        return (
            x1 < x2 + grade_bounding_box_size and
            x1 + grade_bounding_box_size > x2 and
            y1 < y2 + grade_bounding_box_size and
            y1 + grade_bounding_box_size > y2)

    def handle_collision(self, grade_type): # 학점 유형에 따라 충돌 처리
        grade_points = {"A": 4, "B": 3, "C": 2, "D": 1, "F": -2, "F2": -2}

        if grade_type in grade_points:
            self.score += grade_points[grade_type]
            self.coin+= grade_points[grade_type]
        self.score_label.config(text=f"점수: {self.score}")
        self.coin_label.config(text=f"코인: {self.coin}")

    def update_time(self): # 남은 시간 표시
        cur_time = time.time()
        el_time = cur_time - self.start_time
        remaining_time = max(0, self.play_time - el_time)
        seconds = int(remaining_time)
        time_str = f"남은 시간: 00:{seconds:02d}"
        self.time_label.config(text=time_str)
    
    def start_animation(self): # 게임 중 애니메이션
        if not self.game_running: # 게임 끝나면 함수 스킵
            return
        cur_time = time.time()
        el_time = cur_time - self.start_time
        if el_time < self.play_time:
            self.master.after(500, self.update_time)  # 0.5초 후 남은 시간 업데이트
            self.master.after(500, self.start_animation)  # 0.5초 후 함수 재시작

    def end_game(self): # 게임 종료
        global coin
        self.game_running = False
        self.game_pg.pack_forget()
        self.UI.pack_forget()
        self.end_pg.pack()
        texts = [("최종 점수", self.score, 230), ("획득한 코인 수", self.coin, 330)]
        for text, value, y in texts:
            result_text = tkinter.Text(self.end_pg, font=("나무", 40, "bold"), height=1, width=16)
            result_text.insert(tkinter.END, f"{text}: {value}개")
            result_text.place(x=400, y=y)
        
        coin+=self.coin
        coin_label.config(text=f"x {coin}")
    
    def play_game(self):
        self.game_running=True
        self.start_time=time.time()
        self.master.after(1000, self.spawn_grade)
        self.start_animation()
        self.master.after(30000,self.end_game)

class Store:
    def __init__(self, root):
        global coin, mp, hp, energy
        self.root = root
        self.root.title("§§§ 미역 상점 §§§")

        # 이미지 + 캔버스 변수들
        self.bg_img = tkinter.PhotoImage(file="map_store.png") #미역+대화창 있는 배경     #self.npc_img = tk.PhotoImage(file="Miyeok.png") #미역 따로
        self.next_img = tkinter.PhotoImage(file="event_next.png")
        self.coin_img = tkinter.PhotoImage(file="coin_budget.png")
        self.store_pg = tkinter.Canvas(root, width=1600, height=896)
        self.store_pg.pack()
        self.bg = self.store_pg.create_image(800, 448, image=self.bg_img)     #self.npc = self.store_pg.create_image(450, 350, image=self.npc_img) #미역 이미지
        self.next = self.store_pg.create_image(710, 805, image=self.next_img, tags="next")
        self.coin = self.store_pg.create_image(800, 80, image=self.coin_img)
        self.out_btn=tkinter.Button(self.store_pg,text="나가기",font=("나무",36,"bold"),width=6,command=self.after_out_btn)
        self.out_btn.place(x=3,y=3)

        # 보유 수 위젯들
        self.iC_have = self.store_pg.create_text(905, 142, text = f'현재 보유 수: {mp}', font=("맑은 고딕", 10, "bold"), justify="left", anchor="w", fill="gray")
        self.iL_have = self.store_pg.create_text(1225, 144, text = f'현재 보유 수: {hp}', font=("맑은 고딕", 10, "bold"), justify="left", anchor="w", fill="gray")
        self.iD_have = self.store_pg.create_text(905, 516, text = f'현재 보유 수: {energy}', font=("맑은 고딕", 10, "bold"), justify="left", anchor="w", fill="gray")
        self.coin_have = self.store_pg.create_text(775, 80, text = f'{coin}', font=("맑은 고딕", 30, "bold"), anchor="e", fill="white")
        # charge item 관련
        self.cnt_C, self.cnt_L, self.cnt_D, self.cnt_R = 0, 0, 0, 0
        self.plus_C = self.store_pg.create_rectangle(880, 370, 880+25, 370+25, width=0, tags="plus_C") 
        self.minus_C = self.store_pg.create_rectangle(880, 398, 880+25, 398+25, width=0, tags="minus_C")
        self.buy_C = self.store_pg.create_rectangle(1074, 365, 1074+80, 365+60, width=0, tags="purchase_C")
        self.cnt_show_C = self.store_pg.create_text(1010, 392, text=self.cnt_C, font=("맑은 고딕", 30, "bold"), anchor="e")
        self.store_pg.tag_bind("plus_C", '<Button-1>', lambda e: self.plus("C"))
        self.store_pg.tag_bind("minus_C", '<Button-1>', lambda e: self.minus("C"))
        self.store_pg.tag_bind("purchase_C", '<Button-1>', lambda e: self.purchase("C"))
        # life item 관련
        self.plus_L = self.store_pg.create_rectangle(1198, 369, 1198+25, 369+25, width=0, tags="plus_L") 
        self.minus_L = self.store_pg.create_rectangle(1198, 397, 1198+25, 397+25, width=0, tags="minus_L")
        self.buy_L = self.store_pg.create_rectangle(1392, 364, 1392+80, 364+60, width=0, tags="purchase_L")
        self.cnt_show_L = self.store_pg.create_text(1325, 392, text=self.cnt_L, font=("맑은 고딕", 30,  "bold"), anchor="e")
        self.store_pg.tag_bind("plus_L", '<Button-1>', lambda e: self.plus("L"))
        self.store_pg.tag_bind("minus_L", '<Button-1>', lambda e: self.minus("L"))
        self.store_pg.tag_bind("purchase_L", '<Button-1>', lambda e: self.purchase("L"))
        # damage item 관련
        self.plus_D = self.store_pg.create_rectangle(879, 743, 879+25, 743+25, width=0, tags="plus_D") 
        self.minus_D = self.store_pg.create_rectangle(879, 771, 879+25, 771+25, width=0, tags="minus_D")
        self.buy_D = self.store_pg.create_rectangle(1073, 738, 1073+80, 738+60, width=0, tags="purchase_D")
        self.cnt_show_D = self.store_pg.create_text(1010, 767, text=self.cnt_D, font=("맑은 고딕", 30,  "bold"), anchor="e")
        self.store_pg.tag_bind("plus_D", '<Button-1>', lambda e: self.plus("D"))
        self.store_pg.tag_bind("minus_D", '<Button-1>', lambda e: self.minus("D"))
        self.store_pg.tag_bind("purchase_D", '<Button-1>', lambda e: self.purchase("D"))
        # random box item 관련
        self.plus_R = self.store_pg.create_rectangle(1196, 743, 1196+25, 743+25, width=0, tags="plus_R") 
        self.minus_R = self.store_pg.create_rectangle(1196, 771, 1196+25, 771+25, width=0, tags="minus_R")
        self.buy_R = self.store_pg.create_rectangle(1390, 738, 1390+80, 738+60, width=0, tags="purchase_R")
        self.cnt_show_R = self.store_pg.create_text(1325, 767, text=self.cnt_R, font=("맑은 고딕", 30, "bold"), anchor="e")
        self.store_pg.tag_bind("plus_R", '<Button-1>', lambda e: self.plus("R"))
        self.store_pg.tag_bind("minus_R", '<Button-1>', lambda e: self.minus("R"))
        self.store_pg.tag_bind("purchase_R", '<Button-1>', lambda e: self.purchase("R"))
        
        # 입장 시 텍스트 설정
        self.text_idx = 0 
        self.text_cnt_C, self.text_cnt_L, self.text_cnt_D = 0, 0, 0
        self.text_list = ["어서와, 미역 상점은 처음이지?","나는 미역국의 수호 요정이야.\n만나서 반가워 강냉아! ;)", "여기선 아이템을 원하는 수만큼 구매할 수 있어.\n가챠도 있으니 마음껏 즐기다 가라구~! XD"]
        self.root.bind("<z>", lambda e: self.display_text())
        self.display_text()
        
    def after_out_btn(self):
        self.root.destroy()
        close_toplevel()

    def display_text(self): # 텍스트 출력
        if self.text_idx == 2: # 리스트 세 번째를 띄우고 정지
            selected_text = self.text_list[2]
            self.store_pg.delete("next")
        else:
            selected_text = self.text_list[self.text_idx % len(self.text_list)]
            self.text_idx = (self.text_idx + 1) % len(self.text_list)
        self.store_pg.delete("text_display")
        self.store_pg.create_text(70, 640, text=selected_text, font=("맑은 고딕", 25), fill="black", anchor="nw", tag="text_display")

    def plus(self, item_type): # (+)버튼 누를 시
        if item_type == "C":
            self.cnt_C = min(self.cnt_C + 1, coin//65)
            self.store_pg.itemconfig(self.cnt_show_C, text=f'{self.cnt_C}')
        elif item_type == "L":
            self.cnt_L = min(self.cnt_L + 1, coin//30)
            self.store_pg.itemconfig(self.cnt_show_L, text=f'{self.cnt_L}')
        elif item_type == "D":
            self.cnt_D = min(self.cnt_D + 1, coin//40)
            self.store_pg.itemconfig(self.cnt_show_D, text=f'{self.cnt_D}')
        elif item_type == "R":
            self.cnt_R = min(self.cnt_R + 1, coin//45)
            self.store_pg.itemconfig(self.cnt_show_R, text=f'{self.cnt_R}')

    def minus(self, item_type): # (-)버튼 누를 시
        if item_type == "C":
            self.cnt_C = max(0, self.cnt_C - 1)
            self.store_pg.itemconfig(self.cnt_show_C, text=f'{self.cnt_C}')
        elif item_type == "L":
            self.cnt_L = max(0, self.cnt_L - 1)
            self.store_pg.itemconfig(self.cnt_show_L, text=f'{self.cnt_L}')
        elif item_type == "D":
            self.cnt_D = max(0, self.cnt_D - 1)
            self.store_pg.itemconfig(self.cnt_show_D, text=f'{self.cnt_D}')
        elif item_type == "R":
            self.cnt_R = max(0, self.cnt_R - 1)
            self.store_pg.itemconfig(self.cnt_show_R, text=f'{self.cnt_R}')

    def purchase(self, item_type): # (구매)버튼 누를 시
        global coin, mp, energy, hp
        if item_type == "C" and self.cnt_C > 0:
            coin = coin - (self.cnt_C * 65)
            mp = mp + self.cnt_C
            mp_label.config(text=f"x {mp}")
            coin_label.config(text=f"x {coin}")
            self.update_text_else()
        elif item_type == "L" and self.cnt_L > 0:
            coin = coin - (self.cnt_L * 30)
            hp = hp + self.cnt_L
            hp_label.config(text=f"x {hp}")
            coin_label.config(text=f"x {coin}")
            self.update_text_else()
        elif item_type == "D" and self.cnt_D > 0:
            coin = coin - (self.cnt_D * 40)
            energy = energy + self.cnt_D
            energy_label.config(text=f"x {energy}")
            coin_label.config(text=f"x {coin}")
            self.update_text_else()
        elif item_type == "R" and self.cnt_R > 0: # 랜덤박스만 다르게 적용
            coin = coin - (self.cnt_R * 45)
            coin_label.config(text=f"x {coin}")
            for i in range(self.cnt_R):
                self.result = random.randint(1, 10) # 범위를 늘려 극단적인 확률로 조정 가능
                if self.result == 10: # 가장 비싼 템 10% 확률
                    mp = mp + 1
                    self.text_cnt_C += 1
                    mp_label.config(text=f"x {mp}")
                elif self.result < 7 and self.result > 0: # 제일 싼 템 60% 확률
                    hp = hp + 1
                    self.text_cnt_L += 1
                    hp_label.config(text=f"x {hp}")
                elif self.result < 10 and self.result > 6: # 중간 템 30%
                    energy = energy + 1
                    self.text_cnt_D += 1
                    energy_label.config(text=f"x {energy}")
            self.update_text_R()
        self.store_pg.itemconfig(self.iC_have, text=f'현재 보유 수: {mp}')
        self.store_pg.itemconfig(self.iL_have, text=f'현재 보유 수: {hp}')
        self.store_pg.itemconfig(self.iD_have, text=f'현재 보유 수: {energy}')

    def reset(self): # 카운팅 변수들 리셋 + 위젯 갱신
        self.cnt_C, self.cnt_L, self.cnt_D, self.cnt_R = 0, 0, 0, 0
        self.store_pg.itemconfig(self.cnt_show_C, text=f'{self.cnt_C}')
        self.store_pg.itemconfig(self.cnt_show_L, text=f'{self.cnt_L}')
        self.store_pg.itemconfig(self.cnt_show_D, text=f'{self.cnt_D}')
        self.store_pg.itemconfig(self.cnt_show_R, text=f'{self.cnt_R}')
        self.store_pg.itemconfig(self.coin_have, text=f'{coin}')

    def update_text_R(self): # 랜덤박스 구매 시 텍스트 변화(자동으로 스킵 됨)
        self.reset()
        self.text_R = f"와! 상자에서\n필살기 {self.text_cnt_C}개, 회복 {self.text_cnt_L}개, 데미지 {self.text_cnt_D}개가 나왔어.\n정말 대단한걸~~?"
        self.store_pg.delete("text_display")
        self.store_pg.create_text(70, 640, text=self.text_R, font=("맑은 고딕", 25), fill="black", anchor="nw", tag="text_display")
        self.text_cnt_C, self.text_cnt_L, self.text_cnt_D = 0, 0, 0
        if hasattr(self, "text_display"): # after 시간이 지나기 전 연속 클릭 시 빠르게 텍스트가 사라짐을 방지(너무 빠르게 누르면 자주 씹힘)
            self.root.after_cancel(self.timer_R)
            self.root.after_cancel(self.timer_else)
        self.timer_R = self.root.after(4000, self.display_text)
        
    def update_text_else(self): # 일반템 구매 시 텍스트 변화(자동으로 스킵 됨)
        self.reset()
        self.text_else = "구매 고마워~\n적절한 타이밍에 사용해 봐.\n전투에 큰 도움이 될거야."
        self.store_pg.delete("text_display")
        self.store_pg.create_text(70, 640, text=self.text_else, font=("맑은 고딕", 25), fill="black", anchor="nw", tag="text_display")
        if hasattr(self, "text_display"): # after 시간이 지나기 전 연속 클릭 시 빠르게 텍스트가 사라짐을 방지(너무 빠르게 누르면 자주 씹힘)
            self.root.after_cancel(self.timer_else)
            self.root.after_cancel(self.timer_R)
        self.timer_else = self.root.after(2000, self.display_text)

def close_toplevel(): # 미니게임 종료
    root.config(cursor="")
    draw_map()
    draw_item()

# 키 , 마우스 입력
def key_press(e):
    global key
    key=e.keysym
    if key=='z' and canvas.find_withtag("STORY"):
        show_story() 
def key_up(e):
    global key
    key=""
def mouse_move(e):
    global mouseX , mouseY
    mouseX=e.x
    mouseY=e.y
def mouse_click(e):
    global mouseC
    mouseC=1
def mouse_release(e):
    global mouseC
    mouseC=0

# 위젯 요소 생성 및 제거
def delete_text():  # 화면에 나타난 텍스트 지우기
    canvas.delete("TEXT")
def make_text():    # 텍스트 위젯 생성
    left_text.place(x=130,y=550)
    right_text.place(x=980,y=550)
    right_text.delete("1.0","end")
    left_text.delete("1.0", "end")
    canvas.create_image(620,527,image=next_img,tag="NEXT")
def remove_text():  # 텍스트 위젯 제거
    left_text.place_forget()
    right_text.place_forget()

# 게임 시작 초반부에만 사용하는
def show_story():   # 시작 버튼 누른 뒤 스토리 만화
    global story_index
    if story_index<len(story):
        current_story=story[story_index]
        canvas.create_image(800,448,image=current_story,tag="STORY")
        canvas.create_image(1520,850,image=next_img,tag="NEXT")
        story_index+=1
    else:
        canvas.delete("all")
        canvas.create_image(800,448,image=select_chr,tag="Select") # 스토리 끝나면 캐릭선택 창
        make_cursor()
def yes():          # 캐릭 선택 확인 창
    draw_map()
    main_proc()
def make_cursor():  # 캐릭터 선택창 : 이미지 클릭하면 해당 캐릭터로 시작하게 만들 것
    global chr_num, mouseC , mx , my
    if canvas.find_withtag("Select"):
        if 48<=mouseX and mouseX<48+32*11 and 16<=mouseY and mouseY<16+32*17:
            canvas.create_image(224,288,image=cursor_chr,tag="CURSOR")
            canvas.create_image(750,650,image=chr_battle[0],tag="CURSOR")
            canvas.create_image(880,800,image=chr_move[0][0],tag="CURSOR")
            if mouseC==1:
                answer=messagebox.askyesno("캐릭터 선택","'King승헌' 캐릭터를 선택하시겠습니까?")
                if answer:
                    chr_num=0
                    yes()

        elif 48+32*12<=mouseX and mouseX<48+32*23 and 16<=mouseY and mouseY<16+32*17:
            canvas.create_image(608,288,image=cursor_chr,tag="CURSOR")
            canvas.create_image(750,650,image=chr_battle[1],tag="CURSOR")
            canvas.create_image(880,800,image=chr_move[1][0],tag="CURSOR")
            if mouseC==1:
                answer=messagebox.askyesno("캐릭터 선택","'Clown지민' 캐릭터를 선택하시겠습니까?")
                if answer:
                    chr_num=1
                    yes()

        elif 48+32*24<=mouseX and mouseX<48+32*35 and 16<=mouseY and mouseY<16+32*17:
            canvas.create_image(992,288,image=cursor_chr,tag="CURSOR")
            canvas.create_image(750,650,image=chr_battle[2],tag="CURSOR")
            canvas.create_image(880,800,image=chr_move[2][0],tag="CURSOR")
            if mouseC==1:
                answer=messagebox.askyesno("캐릭터 선택","'Baby민서' 캐릭터를 선택하시겠습니까?")
                if answer:
                    chr_num=2
                    yes()

        elif 48+32*36<=mouseX and mouseX<48+32*47 and 16<=mouseY and mouseY<16+32*17:
            canvas.create_image(1376,288,image=cursor_chr,tag="CURSOR")
            canvas.create_image(750,650,image=chr_battle[3],tag="CURSOR")
            canvas.create_image(880,800,image=chr_move[3][0],tag="CURSOR")
            if mouseC==1:
                answer=messagebox.askyesno("캐릭터 선택","'Oldest병찬' 캐릭터를 선택하시겠습니까?")
                if answer:
                    chr_num=3
                    yes()
        else:
            canvas.delete("CURSOR")
    canvas.after(3,make_cursor)

def click_endbtn():
    root.destroy()
def click_startbtn():
    startbtn.place_forget()
    endbtn.place_forget()
    canvas.delete("BG")
    show_story()

# 게임 중 상시 사용
def move():       # 이동기 함수 / 맵 이동 이미지 표시 / 상호작용 이미지 표시
    global mx , my , chr_num, map_num
    if key=="Up" and my>0 and (map_list[map_num][my-1][mx]!=0) and canvas.find_withtag("CHR"):
        my=my-1
        canvas.delete("CHR")
        canvas.create_image(mx*32+16,my*32+16,image=chr_move[chr_num][1],tag="CHR")
    if key=="Down" and my<27 and (map_list[map_num][my+1][mx]!=0) and canvas.find_withtag("CHR"):
        my=my+1
        canvas.delete("CHR")
        canvas.create_image(mx*32+16,my*32+16,image=chr_move[chr_num][0],tag="CHR")
    if key=="Left" and mx>0 and (map_list[map_num][my][mx-1]!=0) and canvas.find_withtag("CHR"):
        mx=mx-1
        canvas.delete("CHR")
        canvas.create_image(mx*32+16,my*32+16,image=chr_move[chr_num][2],tag="CHR")
    if key=="Right" and mx<49 and (map_list[map_num][my][mx+1]!=0) and canvas.find_withtag("CHR"):
        mx=mx+1
        canvas.delete("CHR")
        canvas.create_image(mx*32+16,my*32+16,image=chr_move[chr_num][3],tag="CHR")

    if map_list[map_num][my][mx] in (2,3,4,5,6,11) and not canvas.find_withtag("MAPMOVE"):
        canvas.create_image(mx*32+16,my*32-65,image=mapmove_img,tag="MAPMOVE")
    elif map_list[map_num][my][mx] not in (2,3,4,5,6,11):
        canvas.delete("MAPMOVE")

    if map_list[map_num][my][mx] in (7,8,9,10) and not canvas.find_withtag("CHAT") and canvas.find_withtag("CHR"): #상호작용 도우미
        canvas.create_image(mx*32+16,my*32+65,image=chatnpc_img,tag="CHAT")
    elif map_list[map_num][my][mx] not in (7,8,9,10):
        canvas.delete("CHAT")
def draw_map():   # 맵 이동 후 다음 맵 출력
    canvas.delete("all")
    canvas.create_image(800,448,image=map_img[map_num],tag="MAP")
    canvas.create_image(mx*32+16,my*32+16,image=chr_move[chr_num][0],tag="CHR")
    canvas.update()
    
# 칸 변경
def change_to_eight(): # 상호작용칸 8로 변경
    for y in range(28):
        for x in range(50):
            if map_list[map_num][y][x]==9:
                map_list[map_num][y][x]=8
def change_to_nine():  # 상호작용칸 9로 변경 (캐릭터 사망 시 초기화할때 사용)
    for m in range(6):
        for y in range(28):
            for x in range(50):
                if map_list[m][y][x]==8:
                    map_list[m][y][x]=9
def change_to_ten():   # 상호작용칸 10로 변경 (상자를 까면 변함)
    for y in range(28):
        for x in range(50):
            if map_list[map_num][y][x]==7:
                map_list[map_num][y][x]=10
def change_to_seven(): # 상호작용칸 7로 변경 (사망 시 다시 상자 이벤트 칸으로)
    for m in range(6):
        for y in range(28):
            for x in range(50):
                if map_list[m][y][x]==10:
                    map_list[m][y][x]=7
                
# 전투 요소
def battle_cursor():  # 스킬 위에 커서 표시
    if canvas.find_withtag("BATTLE"):
        if 40*32<=mouseX and mouseX<44*32 and 18*32<=mouseY and mouseY<22*32:     # 할퀴기
            canvas.create_image(42*32,20*32,image=cursor_skill,tag="CURSOR")
            canvas.create_image(43*32,15*32+20,image=explain_skill1[0],tag="CURSOR")
        elif 45*32<=mouseX and mouseX<49*32 and 18*32<=mouseY and mouseY<22*32:   # 깨물기
            canvas.create_image(47*32,20*32,image=cursor_skill,tag="CURSOR")
            canvas.create_image(46*32,15*32+20,image=explain_skill1[1],tag="CURSOR")
        elif 40*32<=mouseX and mouseX<44*32 and 23*32<=mouseY and mouseY<27*32:   # 스킬
            canvas.create_image(42*32,25*32,image=cursor_skill,tag="CURSOR")
            canvas.create_image(43*32,20*32+20,image=explain_skill2[chr_num],tag="CURSOR")
        elif 45*32<=mouseX and mouseX<49*32 and 23*32<=mouseY and mouseY<27*32:   # 도망치기
            canvas.create_image(47*32,25*32,image=cursor_skill,tag="CURSOR")
            canvas.create_image(46*32,20*32+20,image=explain_skill1[2],tag="CURSOR")
        elif 31*32<=mouseX and mouseX<33*32 and 25*32<=mouseY and mouseY<27*32:   # hp
            canvas.create_image(32*32,26*32,image=cursor_item,tag="CURSOR")
            canvas.create_image(33*32,23*32+10,image=explain_item[0],tag="CURSOR")
        elif 34*32<=mouseX and mouseX<36*32 and 25*32<=mouseY and mouseY<27*32:   # mp
            canvas.create_image(35*32,26*32,image=cursor_item,tag="CURSOR")
            canvas.create_image(36*32,23*32+10,image=explain_item[1],tag="CURSOR")
        elif 37*32<=mouseX and mouseX<39*32 and 25*32<=mouseY and mouseY<27*32:   # 공업
            canvas.create_image(38*32,26*32,image=cursor_item,tag="CURSOR")
            canvas.create_image(39*32,23*32+10,image=explain_item[2],tag="CURSOR")
        else:
            canvas.delete("CURSOR")
    else:
        canvas.delete("CURSOR")
    canvas.after(10,battle_cursor)
def scratch():     # 공격력(power)만큼 공격
    if canvas.find_withtag("BATTLE"):    
        if 40*32<=mouseX and mouseX<44*32 and 18*32<=mouseY and mouseY<22*32:
            if mouseC==1:
                character[chr_num].gauge+=1
                if character[chr_num].gauge>=4:
                    character[chr_num].gauge=4
                character[chr_num].attack_motion()
                play_atk('atk1')
                chr_boss[boss_num].scratch_attack()
                if chr_boss[boss_num].life>0:         # 보스가 공격을 받고도 살아있으면 공격 실행
                    chr_boss[boss_num].attack_motion()
                    character[chr_num].player_damaged()
                check_game_result()
    if not canvas.find_withtag("BATTLE"):
        return
    canvas.after(10,scratch)
def bite():     # 공격력(power)만큼 공격
    if canvas.find_withtag("BATTLE"):    
        if 45*32<=mouseX and mouseX<49*32 and 18*32<=mouseY and mouseY<22*32:
            if mouseC==1:
                character[chr_num].gauge+=1
                if character[chr_num].gauge>=4:
                    character[chr_num].gauge=4
                character[chr_num].attack_motion()
                play_atk('atk2')
                chr_boss[boss_num].bite_attack()
                if chr_boss[boss_num].life>0:  
                    chr_boss[boss_num].attack_motion()
                    character[chr_num].player_damaged()
                check_game_result()
    if not canvas.find_withtag("BATTLE"):
        return
    canvas.after(10,bite)
def skill_atk():   # 스킬 공격
    if canvas.find_withtag("BATTLE"): 
        if 40*32<=mouseX and mouseX<44*32 and 23*32<=mouseY and mouseY<27*32 and character[chr_num].gauge!=4:
            if mouseC==1:
                canvas.create_text(800,400,text="스킬 사용에 필요한 게이지가 부족합니다",font=("휴먼매직체",35),fill="black",tag="TEXT")
                canvas.after(1000,delete_text)
        elif 40*32<=mouseX and mouseX<44*32 and 23*32<=mouseY and mouseY<27*32 and character[chr_num].gauge==4:
            if mouseC==1:
                if chr_num==0:
                    play_atk('beam')
                elif chr_num==1:
                    play_atk('joke')
                elif chr_num==2:
                    play_atk('error')
                else:
                    play_atk('throw')
                character[chr_num].gauge=character[chr_num].gauge-4
                chr_boss[boss_num].special_attack()
                if chr_boss[boss_num].life>0:
                    chr_boss[boss_num].attack_motion()
                    character[chr_num].player_damaged()
                check_game_result()
    if not canvas.find_withtag("BATTLE"):
        return
    canvas.after(10,skill_atk)
def escape(): # 도망치기
    global esc_try,mouseC,boss_num
    if 45*32<=mouseX and mouseX<49*32 and 23*32<=mouseY and mouseY<27*32 and canvas.find_withtag("BATTLE"):
        if mouseC==1:
            if esc_try==0:
                if random.random()<=0.3:
                    esc_try=0
                    escape_success()
                else:
                    canvas.create_text(802,352,text=("도망치는데 실패했다..\n(남은 기회 1번)"),font=("휴먼매직체",45),fill="black",tag="TEXT")
                    canvas.create_text(800,350,text=("도망치는데 실패했다..\n(남은 기회 1번)"),font=("휴먼매직체",45),fill="white",tag="TEXT")
                    canvas.after(1500,delete_text)
                    esc_try+=1
            elif esc_try==1:
                if random.random()<=0.6:
                    esc_try=0
                    escape_success()
                else:
                    canvas.create_text(802,352,text=("도망치는데 실패했다..\n(모든 기회 소진)"),font=("휴먼매직체",45),fill="black",tag="TEXT")
                    canvas.create_text(800,350,text=("도망치는데 실패했다..\n(모든 기회 소진)"),font=("휴먼매직체",45),fill="white",tag="TEXT")
                    canvas.after(1500,delete_text)
                    esc_try+=1
            elif esc_try>=2:
                canvas.create_text(802,352,text=("도망칠 수 있는 기회가 없다"),font=("휴먼매직체",45),fill="black",tag="TEXT")
                canvas.create_text(800,350,text=("도망칠 수 있는 기회가 없다"),font=("휴먼매직체",45),fill="white",tag="TEXT")
                canvas.after(1500,delete_text)
            mouseC=0

    canvas.after(10,escape)
def escape_success():  # 도망 성공 시 이벤트
    canvas.delete("all")
    canvas.update()
    draw_item()
    draw_map()
    canvas.create_text(802,352,text=("도망치는데 성공했다!"),font=("휴먼매직체",45),fill="black",tag="TEXT")
    canvas.create_text(800,350,text=("도망치는데 성공했다!"),font=("휴먼매직체",45),fill="white",tag="TEXT")
    canvas.after(1500,delete_text)
    character[chr_num].life=character[chr_num].lmax
    chr_boss[boss_num].life=chr_boss[boss_num].lmax
    if current_map=="cu":
        for y in range(28):
            for x in range(50):
                if CU_map[y][x]==8:
                    CU_map[y][x]=9
    elif current_map=="classroom":
        for y in range(28):
            for x in range(50):
                if classroom_map[y][x]==8:
                    classroom_map[y][x]=9
    elif current_map=="boss":
        for y in range(28):
            for x in range(50):
                if boss_map[y][x]==8:
                    boss_map[y][x]=9
    play_bgm('bgm1')

def heal():     # HP물약 사용
    global mouseC, hp
    if canvas.find_withtag("BATTLE") and 31*32<=mouseX and mouseX<33*32 and 25*32<=mouseY and mouseY<27*32:
        if mouseC==1:
            if hp>=1:
                if character[chr_num].life>=character[chr_num].lmax:
                    canvas.create_text(800,300,text=("이미 최대 체력입니다"),font=("휴먼매직체",40,"bold"),tag="TEXT")
                    canvas.after(1000,delete_text)
                else:
                    hp=hp-1
                    character[chr_num].life+=50
                    if character[chr_num].life>=character[chr_num].lmax:
                        character[chr_num].life=character[chr_num].lmax
                    character[chr_num].remove_player()
                    character[chr_num].draw_player()
                    canvas.create_text(800,300,text=(f"  HP 50 회복\n(남은 물약 :{hp})"),font=("휴먼매직체",40,"bold"),tag="TEXT")
                    canvas.after(1000,delete_text)
                update_item()
            else:
                canvas.create_text(800,300,text=("HP회복 물약이 없습니다"),font=("휴먼매직체",40,"bold"),tag="TEXT")
                canvas.after(1000,delete_text)
        mouseC=0
    canvas.after(10,heal)
def stamina():  # MP물약 사용
    global mouseC , mp
    if canvas.find_withtag("BATTLE") and 34*32<=mouseX and mouseX<36*32 and 25*32<=mouseY and mouseY<27*32:
        if mouseC==1:
            if mp>=1:
                if character[chr_num].gauge==4:
                    canvas.create_text(800,300,text=("이미 MP가 꽉 차있습니다"),font=("휴먼매직체",40,"bold"),tag="TEXT")
                    canvas.after(1000,delete_text)
                else:
                    mp=mp-1
                    character[chr_num].gauge+=4
                    if character[chr_num].gauge>=4:
                        character[chr_num].gauge=4
                    character[chr_num].remove_player()
                    character[chr_num].draw_player()
                    canvas.create_text(800,300,text=(f"    MP 회복\n(남은 물약 :{mp})"),font=("휴먼매직체",40,"bold"),tag="TEXT")
                    canvas.after(1000,delete_text)
                update_item()
            else:
                canvas.create_text(800,300,text=("MP회복 물약이 없습니다"),font=("휴먼매직체",40,"bold"),tag="TEXT")
                canvas.after(1000,delete_text)
        mouseC=0
    canvas.after(10,stamina)
def power_up(): # 공업 사용
    global mouseC, energy
    if canvas.find_withtag("BATTLE") and 37*32<=mouseX and mouseX<39*32 and 25*32<=mouseY and mouseY<27*32:
        if mouseC==1:
            if energy>=1:
                energy=energy-1
                character[chr_num].power+=20
                canvas.create_text(800,300,text=(f"이번 전투에서 공격력이 20상승합니다\n          (현재공격력{character[chr_num].power})"),font=("휴먼매직체",40,"bold"),tag="TEXT")
                canvas.after(1000,delete_text)
                update_item()
            else:
                canvas.create_text(800,300,text=(f"공격력 증가 아이템이 없습니다\n      (현재공격력{character[chr_num].power})"),font=("휴먼매직체",40,"bold"),tag="TEXT")
                canvas.after(1000,delete_text)
        mouseC=0
    canvas.after(10,power_up)

# 음악 재생
bgm_files={'bgm1':'bgm.ogg','bgm2':'bgm_boss1.ogg','bgm3':'bgm_boss2.ogg','bgm4':'bgm_boss3.ogg'}
atk_files={'atk1':'sound_atk1.ogg','atk2':'sound_atk2.ogg',
           'beam':'sound_beam.ogg','joke':'sound_joke.ogg','error':'sound_error.ogg','throw':'sound_throw.ogg',}
pygame.init()
pygame.mixer.init()
bgm_channel=pygame.mixer.Channel(0)
atk_channel=pygame.mixer.Channel(1)
def play_bgm(music_key):
    bgm_channel.stop()
    bgm_sound=pygame.mixer.Sound(bgm_files[music_key])
    bgm_channel.play(bgm_sound,loops=-1)
    bgm_channel.set_volume(0.60)
def play_atk(music_key):
    atk_sound=pygame.mixer.Sound(atk_files[music_key])
    atk_channel.play(atk_sound)
    atk_channel.set_volume(1)

# 메인 프로그램
def main_proc():
    global mx, my, chr_num,  current_map, map_num , boss_num , catch_boss
#상호작용
    if current_map=="home":
        draw_item()
        map_num=0
        move()
        chest()
    
    if current_map=="school":
        map_num=1
        move()
        chest()
    
    if current_map=="cu":
        map_num=2
        boss_num=0
        move()
        chest()

        if CU_map[my][mx]==9 and key=="space" and catch_boss==0:                     # 학생회와 전투
            play_bgm('bgm2')
            remove_item() 
            change_to_eight()
            canvas.delete("all")
            canvas.update()

            canvas.create_image(800,448,image=ChatMap[boss_num],tag="chat_screen")
            character[chr_num].chat_draw()
            chr_boss[boss_num].chat_draw()
            make_text()
            root.bind("<z>", lambda event: before_war(event, before[boss_num]))
            root.bind("<Z>", lambda event: before_war(event, before[boss_num]))

        if CU_map[my][mx]==8 and key=="space" and catch_boss>=1:   # 승리 후 학생회와 대화
            remove_item()
            canvas.create_image(800,448,image=ChatMap[boss_num],tag="chat_screen")
            character[chr_num].chat_draw()
            chr_boss[boss_num].chat_draw()
            make_text()
            root.bind("<z>", lambda event: after_war(event, after[boss_num]))
            root.bind("<Z>", lambda event: after_war(event, after[boss_num]))

    if current_map=="classroom":
        map_num=3
        boss_num=1
        move()
        chest()

        if key=="space" and classroom_map[my][mx]==9:              # 교수님과 상호작용
            if catch_boss!=1:                                      # 학생회 쓰러트리기 이전
                canvas.create_text(802,450,text="CU에서 학생회를 먼저 물리치자!!",font=("휴먼매직체",50),fill="black",tag="TEXT")
                canvas.create_text(800,448,text="CU에서 학생회를 먼저 물리치자!!",font=("휴먼매직체",50),fill="white",tag="TEXT")
                canvas.after(2500,delete_text)

            elif catch_boss==1:                                    # 교수님과 전투
                play_bgm('bgm3')
                remove_item() 
                change_to_eight()
                canvas.delete("all")
                canvas.update()

                canvas.create_image(800,448,image=ChatMap[boss_num],tag="chat_screen")
                character[chr_num].chat_draw()
                chr_boss[boss_num].chat_draw()
                make_text()
                root.bind("<z>", lambda event: before_war(event, before[boss_num]))
                root.bind("<Z>", lambda event: before_war(event, before[boss_num]))
        
        if key=="space" and classroom_map[my][mx]==8 and catch_boss>=2:  # 승리 후 교수님과 대화
            remove_item()
            canvas.create_image(800,448,image=ChatMap[boss_num],tag="chat_screen")
            character[chr_num].chat_draw()
            chr_boss[boss_num].chat_draw()
            make_text()
            root.bind("<z>", lambda event: after_war(event, after[boss_num]))
            root.bind("<Z>", lambda event: after_war(event, after[boss_num]))

    if current_map=="boss":
        map_num=4
        boss_num=2
        move()
        chest()

        if key=="space" and boss_map[my][mx]==9: #총장님과 상호작용
            if catch_boss==0:   # 학생회 / 교수님 잡기 전 상호작용 시
                canvas.create_text(802,450,text="학생회와 교수님을 먼저 물리치자!!",font=("휴먼매직체",50),fill="black",tag="TEXT")
                canvas.create_text(800,448,text="학생회와 교수님을 먼저 물리치자!!",font=("휴먼매직체",50),fill="white",tag="TEXT")
                canvas.after(3500,delete_text)

            elif catch_boss==1:
                canvas.create_text(802,450,text="교수님을 먼저 물리치자!!",font=("휴먼매직체",50),fill="black",tag="TEXT")
                canvas.create_text(800,448,text="교수님을 먼저 물리치자!!",font=("휴먼매직체",50),fill="white",tag="TEXT")
                canvas.after(2500,delete_text)
            
            elif catch_boss==2:
                play_bgm('bgm4')
                remove_item() 
                change_to_eight()
                canvas.delete("all")
                canvas.update()
                
                canvas.create_image(800,448,image=ChatMap[boss_num],tag="chat_screen")
                character[chr_num].chat_draw()
                chr_boss[boss_num].chat_draw()
                make_text()
                root.bind("<z>", lambda event: before_war(event, before[boss_num]))
                root.bind("<Z>", lambda event: before_war(event, before[boss_num]))
            
        if key=="space" and boss_map[my][mx]==8 and catch_boss>=3:  # 총장님과 승리 후 대화
            remove_item()
            canvas.create_image(800,448,image=ChatMap[boss_num],tag="chat_screen")
            character[chr_num].chat_draw()
            chr_boss[boss_num].chat_draw()
            make_text()
            root.bind("<z>", lambda event: after_war(event, after[boss_num]))
            root.bind("<Z>", lambda event: after_war(event, after[boss_num]))
        
        if key=="space" and boss_map[my][mx]==4:  # 엔딩 장면
            if catch_boss<3:
                canvas.create_text(802,450,text="모든 보스를 먼저 물리치자!!",font=("휴먼매직체",50),fill="black",tag="TEXT")
                canvas.create_text(800,448,text="모든 보스를 먼저 물리치자!!",font=("휴먼매직체",50),fill="white",tag="TEXT")
                canvas.after(2500,delete_text)
            else:
                mx,my=0,0
                canvas.delete("all")
                canvas.delete("MAPMOVE")
                remove_item()
                canvas.create_image(800,448,image=ending_img)
                button=tkinter.Button(root,text="게임종료",font=("휴먼매직체",40,"bold"),fg="black",width=8,command=click_endbtn)
                button.place(x=690,y=780)
                
    if current_map=="gameroom":
        map_num=5
        move()
        chest()
        if game_map[my][mx]==3 and key=="space": #민서게임
            mx,my=8,8
            canvas.delete("CHR")
            remove_item()
            game1=tkinter.Toplevel(root)
            game_instance=Targetgame(game1)
            game1.protocol("WM_DELETE_WINDOW",lambda: None)
        
        if game_map[my][mx]==4 and key=="space": #민서게임
            mx,my=25,8
            canvas.delete("CHR")
            remove_item()
            game2=tkinter.Toplevel(root)
            game_instance=PackMan(game2)
            game2.protocol("WM_DELETE_WINDOW",lambda: None)
        
        if game_map[my][mx]==5 and key=="space": #민서게임
            mx,my=41,8
            canvas.delete("CHR")
            remove_item()
            game3=tkinter.Toplevel(root)
            game_instance=CollegeGame(game3)
            game3.protocol("WM_DELETE_WINDOW",lambda: None)
    
#이동관련
    if current_map=="home":       # home > school
        if key=="space" and (map_list[map_num][my][mx]==5):
            mx=6
            my=26
            map_num=1
            current_map="school"
            draw_map()

    if current_map=="school":     # school > (home / CU / classroom / boss / gameroom / store)
        if key=="space" and (school_map[my][mx]==2):
            mx=43
            my=27
            map_num=0
            current_map="home"
            draw_map()
        elif key=="space" and (school_map[my][mx]==5):
            mx=40
            my=25
            map_num=2
            current_map="cu"
            draw_map()
        elif key=="space" and (school_map[my][mx]==3):
            mx=44
            my=25
            map_num=3
            current_map="classroom"
            draw_map()
        elif key=="space" and (school_map[my][mx]==6):
            mx=49
            my=24
            map_num=4
            current_map="boss"
            draw_map()
        elif key=="space" and (school_map[my][mx]==4):
            mx=25
            my=24
            map_num=5
            current_map="gameroom"
            draw_map()
        elif key=="space" and (school_map[my][mx]==11):
            map_num=1
            mx,my=37,25
            canvas.delete("CHR")
            remove_item()
            instore=tkinter.Toplevel(root)
            store_instance=Store(instore)
            instore.protocol("WM_DELETE_WINDOW",lambda: None)

    if current_map=="cu":         # cu > school
        if key=="space" and (CU_map[my][mx]==5):
            mx=24
            my=11
            map_num=1
            current_map="school"
            draw_map()

    if current_map=="classroom":  # classroom > school
        if key=="space" and (classroom_map[my][mx]==5):
            mx=9
            my=3
            map_num=1
            current_map="school"
            draw_map()

    if current_map=="boss":       # boss > school
        if key=="space" and (boss_map[my][mx]==5):
            mx=24
            my=20
            map_num=1
            current_map="school"
            draw_map()
            
    if current_map=="gameroom":   # gameroom > school
        if key=="space" and (game_map[my][mx]==2):
            mx=44
            my=7
            map_num=1
            current_map="school"
            draw_map()

    root.after(40,main_proc)

# 맵  (map_num : )
home_map=[ # 0=벽 / 1=통로 / 5=포탈 / 7=상자 / 10=상자깐곳
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,7,1,1,0,0,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0], 
    [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,7,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0], 
    [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0], 
    [0,0,0,0,0,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0], 
    [0,0,0,0,0,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0], 
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0], 
    [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,5,5,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,5,5,1,1,0,0,0,0,0]]
school_map=[ # 0=벽 / 1=통로 / 2= 집으로 / 3=이공관 / 4=천은관 / 5=경천관 / 6=본관 / 7=상자 / 11=상점
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0], 
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0], 
    [1,1,1,0,0,0,0,0,0,3,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0], 
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0], 
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0], 
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0], 
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0], 
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,4,0,0,0,0], 
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0], 
    [0,7,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0], 
    [7,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,5,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0], 
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], 
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], 
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1], 
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1], 
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1], 
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], 
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], 
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,6,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1], 
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1], 
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1], 
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], 
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], 
    [0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,1], 
    [0,0,0,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,1,1,1,1,0,0,0,1], 
    [0,0,0,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,0,1,1,1,1,1,1,1,0,0,0,1], 
    [1,1,1,1,1,1,2,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,1,1,1,1,1,1,1,1]]
CU_map=[ #0=벽 / 1=통로 / 5=포탈 / 9=이벤트칸 / 7=상자
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,7,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0], 
    [0,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,0,1,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0], 
    [0,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0], 
    [0,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,0,1,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0], 
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,9,0,1,1,1,0,9,1,1,1,0], 
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,9,0,1,1,1,0,9,1,1,1,0], 
    [0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,1,0,0,0,1,1,1,1,1,1,9,0,0,0,0,0,9,1,1,1,0], 
    [0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,1,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0], 
    [0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,1,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0], 
    [0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0], 
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0], 
    [0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0], 
    [0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0], 
    [0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0], 
    [0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0], 
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0], 
    [0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,1,0,0,0,0], 
    [0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,1,0,0,0,0], 
    [0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,1,0,0,0,0],
    [0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0], 
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0], 
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0], 
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,5,5,1,1,1,0,0,0,0], 
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,5,5,1,1,1,0,0,0,0], 
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
classroom_map=[#0=벽 / 1=통로 / 5=포탈 / 9=이벤트칸 / 7=상자
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
    [0,0,1,1,0,0,0,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0], 
    [0,7,0,0,0,0,0,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0], 
    [0,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,5,5,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,5,5,1,1,1,0]]
boss_map=[ #0=벽 / 1=통로 / 4=엔딩포탈 / 5포탈 / 9=이벤트칸 / 7=상자
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,9,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,9,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,9,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,7,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,0,0,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,0,0,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,0,0,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,0,0,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1],
    [4,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,5],
    [4,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,5],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
game_map=[ #0=벽 / 1=통로 / 2=이전맵 / 3=노랑게임 / 4=빨강게임 / 5=초록게임 / 7=상자
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,0,0,7,1,1,1,1,0],
    [0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0],
    [0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,3,3,3,1,1,1,1,1,1,0,1,1,1,1,1,1,1,4,4,4,1,1,1,1,1,1,0,1,1,1,1,1,1,5,5,5,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,3,3,3,1,1,1,1,1,1,0,1,1,1,1,1,1,1,4,4,4,1,1,1,1,1,1,0,1,1,1,1,1,1,5,5,5,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

map_list=[home_map,school_map,CU_map,classroom_map,boss_map,game_map]

# 캐릭터 대사
before = [["하...;;","너 또 지각이야?", "내가 1학년 때부터 달구지 좀\n늘려달라고 했잖아!!", "우리도 노력한거라구!!\n최선을 다 했거든ㅋ", "으어어ㅓ어ㅓㅓㅓ!!",""],
          ["달구지 때문에 늦은건데\n꼭 지각처리를 하셔야겠어요??", "그럼 집에서 더 일찍 나오시게", "저는 잠이 더 중요하다구요!!ㅠ.ㅠ",""],
          ["총장님 사랑합니다..그러나 But!! 제가 그 자리를 좀 물려받아야겠습니다","어디서 강아지 소리가 들리는구만??",""]]
after_win=[["이제 달구지 늘려줄거지??!","으..윽..우..우리는 권한이 없어..\n교수님을 찾아가봐",""],
           ["교수님 이제 출석 인정\n해주시는거죵??","학생도 알겠지만\n나는 너무 바쁘다네...\n총장님을 찾아가보시게..",""],
           ["총장님 CUT","달구지를 100대 늘려주겠네..","쯧..\n애초에 할 수 있었던 것을..",""]]
after_lose=[["...","ㅋㅋㅋㅋ 돌아가!","하아...두고봐! 강해져서 돌아올테니!"],
            ["...","자네는 F야!! F!!!","안돼애애애애애애애애애~~~ㅜㅜ,,"],
            ["...","넌 퇴학이다",""]]
after=[["또 맞기 싫으면 조심해줘용","ㅜㅜㅠㅜㅠㅜㅠ","확 마",""],
       ["출석 처리는 물론\n성적도 A+로 주셔야 할 겁니다","알겠으니 더는 때리지 말아주게...",""],
       ["헤이헤이!!","옙.. 총장님!!","이제 달구지 늘려주세영","옙...ㅠㅜ",""]]

# 보스와 대화 관련
text_idx=0
def before_war(e,chat_list):  # 텍스트 z로 업데이트 / 대화 끝나면 대화 요소 모두 삭제 후 전투 요소 출력
    global text_idx, esc_try
    selected=chat_list[text_idx % len(chat_list)]
    if text_idx%2==0:                       # 캐릭터 대사
        canvas.delete("ch")                                  # 캐릭터 대사 시 캐릭터 이미지 변경
        character[chr_num].imgfile=chr_chat[chr_num]
        character[chr_num].chat_draw()
        
        canvas.delete("boss")                                # 캐릭터 대사 시 보스 이미지 원상복구
        chr_boss[boss_num].imgfile=boss_chr[boss_num][0]
        chr_boss[boss_num].chat_draw()
        canvas.update()

        left_text.delete("1.0", "end")
        left_text.insert("1.0", selected)
        right_text.delete("1.0","end")
    else:                                   # 보스 대사
        canvas.delete("boss")                                # 보스 대사 시 보스 이미지 변경
        chr_boss[boss_num].imgfile=boss_chat[boss_num][0]
        chr_boss[boss_num].chat_draw()

        canvas.delete("ch")
        character[chr_num].imgfile=chr_battle[chr_num]
        character[chr_num].chat_draw()
        canvas.update()

        right_text.delete("1.0", "end")
        right_text.insert("1.0", selected)
        left_text.delete("1.0", "end")
    text_idx=(text_idx+1)%len(chat_list)

    if text_idx==0:      #대화가 끝나면
        character[chr_num].imgfile=chr_battle[chr_num]
        chr_boss[boss_num].imgfile=boss_chr[boss_num][0]

        esc_try=0
        root.unbind("<z>")
        root.unbind("<Z>")
        canvas.delete("all")
        remove_text()                     #텍스트 위젯 삭제
        character[chr_num].chat_remove()
        chr_boss[boss_num].chat_remove()    #대화 배경 / 캐릭터 삭제
        canvas.update()
        canvas.create_image(800,448,image=battle_map[boss_num],tag="BATTLE")
        battle_cursor()
        scratch()
        bite()
        skill_atk()
        escape()
        heal()
        stamina()
        power_up()
        character[chr_num].draw_player()
        chr_boss[boss_num].draw_boss()        #전투 배경 / 캐릭터 배치
        
def win_war(e,chat_list):     # 전투 이긴 후 대화
    global text_idx , current_map , mx , my , map_num , catch_boss
    selected=chat_list[text_idx % len(chat_list)]

    if text_idx%2==0:                       # 캐릭터 대사
        canvas.delete("ch")                                  # 캐릭터 대사 시 캐릭터 이미지 변경
        character[chr_num].imgfile=chr_chat[chr_num]
        character[chr_num].chat_draw()
        
        canvas.delete("boss")                                # 캐릭터 대사 시 보스 이미지 원상복구
        chr_boss[boss_num].imgfile=boss_chr[boss_num][0]
        chr_boss[boss_num].chat_draw()
        canvas.update()

        left_text.delete("1.0", "end")
        left_text.insert("1.0", selected)
        right_text.delete("1.0","end")
    else:                                   # 보스 대사
        canvas.delete("boss")                                # 보스 대사 시 보스 이미지 변경
        chr_boss[boss_num].imgfile=boss_chat[boss_num][0]
        chr_boss[boss_num].chat_draw()

        canvas.delete("ch")
        character[chr_num].imgfile=chr_battle[chr_num]
        character[chr_num].chat_draw()
        canvas.update()

        right_text.delete("1.0", "end")
        right_text.insert("1.0", selected)
        left_text.delete("1.0", "end")
    text_idx=(text_idx+1)%len(chat_list)

    if text_idx==0:      #원래 맵으로 복귀
        character[chr_num].imgfile=chr_battle[chr_num]
        chr_boss[boss_num].imgfile=boss_chr[boss_num][0]

        root.unbind("<z>")
        root.unbind("<Z>")
        canvas.delete("all")
        play_bgm('bgm1')
        character[chr_num].power=character[chr_num].lpower
        remove_text()
        draw_item()
        draw_map()
        if current_map=="cu": 
            catch_boss=1
        if current_map=="classroom": 
            catch_boss=2
        if current_map=="boss": 
            catch_boss=3
        move()
        
def lose_war(e,chat_list):    # 전투 지고 대화 및 Home에서 다시 시작
    global text_idx,current_map,mx,my , catch_boss , map_num , coin , mp , hp, energy,esc_try
    selected=chat_list[text_idx % len(chat_list)]

    if text_idx%2==0:                       # 캐릭터 대사
        canvas.delete("ch")                                  # 캐릭터 대사 시 캐릭터 이미지 변경
        character[chr_num].imgfile=chr_chat[chr_num]
        character[chr_num].chat_draw()
        
        canvas.delete("boss")                                # 캐릭터 대사 시 보스 이미지 원상복구
        chr_boss[boss_num].imgfile=boss_chr[boss_num][0]
        chr_boss[boss_num].chat_draw()
        canvas.update()

        left_text.delete("1.0", "end")
        left_text.insert("1.0", selected)
        right_text.delete("1.0","end")
    else:                                   # 보스 대사
        canvas.delete("boss")                                # 보스 대사 시 보스 이미지 변경
        chr_boss[boss_num].imgfile=boss_chat[boss_num][0]
        chr_boss[boss_num].chat_draw()

        canvas.delete("ch")
        character[chr_num].imgfile=chr_battle[chr_num]
        character[chr_num].chat_draw()
        canvas.update()

        right_text.delete("1.0", "end")
        right_text.insert("1.0", selected)
        left_text.delete("1.0", "end")
    text_idx=(text_idx+1)%len(chat_list)

    if text_idx==0:      #대화가 끝나면
        character[chr_num].imgfile=chr_battle[chr_num]
        chr_boss[boss_num].imgfile=boss_chr[boss_num][0]

        root.unbind("<z>")
        root.unbind("<Z>")
        canvas.delete("all")
        remove_text()
        canvas.create_image(800,448,image=youdie_img,tag="DIE")
        canvas.update()
        time.sleep(2.5)
        canvas.delete("all")
        canvas.update()

        play_bgm('bgm1')
        change_to_nine()                              # 상호작용 칸 되돌림
        change_to_seven()
        draw_item()
        coin,mp,hp,energy=0,0,0,0                     # 캐릭터 정보 초기화
        update_item()
        mx,my,catch_boss=6,6,0                        
        esc_try=0
        character[chr_num].gauge=2
        character[chr_num].life=character[chr_num].lmax
        chr_boss[0].life=chr_boss[0].lmax             # 보스 HP 초기화
        chr_boss[1].life=chr_boss[1].lmax
        chr_boss[2].life=chr_boss[2].lmax
        current_map="home"                            # 태초 맵 출력
        map_num=0
        draw_map()

def after_war(e,chat_list):   # 한번 더 대화 시
    global text_idx
    selected=chat_list[text_idx % len(chat_list)]
    canvas.delete("CHR")
    remove_item()
    if text_idx%2==0:                       # 캐릭터 대사
        canvas.delete("ch")                                  # 캐릭터 대사 시 캐릭터 이미지 변경
        character[chr_num].imgfile=chr_chat[chr_num]
        character[chr_num].chat_draw()
        
        canvas.delete("boss")                                # 캐릭터 대사 시 보스 이미지 원상복구
        chr_boss[boss_num].imgfile=boss_chr[boss_num][0]
        chr_boss[boss_num].chat_draw()
        canvas.update()

        left_text.delete("1.0", "end")
        left_text.insert("1.0", selected)
        right_text.delete("1.0","end")
    else:                                   # 보스 대사
        canvas.delete("boss")                                # 보스 대사 시 보스 이미지 변경
        chr_boss[boss_num].imgfile=boss_chat[boss_num][0]
        chr_boss[boss_num].chat_draw()

        canvas.delete("ch")
        character[chr_num].imgfile=chr_battle[chr_num]
        character[chr_num].chat_draw()
        canvas.update()

        right_text.delete("1.0", "end")
        right_text.insert("1.0", selected)
        left_text.delete("1.0", "end")
    text_idx=(text_idx+1)%len(chat_list)

    if text_idx==0:      #대화가 끝나면
        character[chr_num].imgfile=chr_battle[chr_num]
        chr_boss[boss_num].imgfile=boss_chr[boss_num][0]
        root.unbind("<z>")
        root.unbind("<Z>")
        canvas.delete("NEXT")
        remove_text()
        character[chr_num].chat_remove()
        chr_boss[boss_num].chat_remove()
        canvas.create_image(mx*32+16,my*32+16,image=chr_move[chr_num][0],tag="CHR")
        draw_item()
        canvas.update()

def check_game_result():      # 전투 승리 / 패배 시
    if character[chr_num].life<=0:   #전투 패배 시 ==> 패배 대화 후 ==> home맵에서 캐릭터 재생성
        canvas.delete("all")
        canvas.update()
        canvas.create_image(800,448,image=ChatMap[boss_num],tag="chat_screen")
        character[chr_num].chat_draw()
        chr_boss[boss_num].chat_draw()
        canvas.update()
        make_text()
        root.bind("<z>", lambda event: lose_war(event, after_lose[boss_num]))
        root.bind("<Z>", lambda event: lose_war(event, after_lose[boss_num]))
            
    if chr_boss[boss_num].life<=0:   #전투 승리 시 >> 승리 대화 후 >> 전투 했던 맵 다시 출력
        canvas.delete("all")
        canvas.update()
        canvas.create_image(800,448,image=ChatMap[boss_num],tag="chat_screen")
        character[chr_num].chat_draw()
        chr_boss[boss_num].chat_draw()
        canvas.update()
        make_text()
        root.bind("<z>", lambda event: win_war(event, after_win[boss_num]))
        root.bind("<Z>", lambda event: win_war(event, after_win[boss_num]))

# 재화 요소
def get_item():    # 상자 랜덤 획득
    global hp,mp,energy
    what=random.choice(items)
    if what=="mp":
        mp+=1
        canvas.create_text(802,202,text=("마나포션을 얻었다!"),font=("휴먼매직체",30),fill="black",tag="TEXT")
        canvas.create_text(800,200,text=("마나포션을 얻었다!"),font=("휴먼매직체",30),fill="blue",tag="TEXT")
        canvas.after(1500,delete_text)
    elif what=="energy":
        energy+=1
        canvas.create_text(802,202,text=("공격력 강화 아이템을 얻었다!"),font=("휴먼매직체",30),fill="black",tag="TEXT")
        canvas.create_text(800,200,text=("공격력 강화 아이템을 얻었다!"),font=("휴먼매직체",30),fill="purple",tag="TEXT")
        canvas.after(1500,delete_text)
    else:
        hp+=1
        canvas.create_text(802,202,text=("회복물약을 얻었다!"),font=("휴먼매직체",30),fill="black",tag="TEXT")
        canvas.create_text(800,200,text=("회복물약을 얻었다!"),font=("휴먼매직체",30),fill="red",tag="TEXT")
        canvas.after(1500,delete_text)
    update_item()
def update_item(): # 아이템 라벨 업데이트
    hp_label.config(text=f"x {hp}")
    mp_label.config(text=f"x {mp}")
    energy_label.config(text=f"x {energy}")
    coin_label.config(text=f"x {coin}")
def chest():       # 상자 열었을 때 함수
    if map_list[map_num][my][mx]==7 and key=="space" and canvas.find_withtag("CHR"):
        get_item()
        change_to_ten()
def draw_item():   # 아이템 갯수 라벨 생성
    hp_label.place(x=1245,y=18)
    mp_label.place(x=1323,y=18)
    energy_label.place(x=1403,y=18)
    coin_label.place(x=1500,y=18)
def remove_item(): # 아이템 라벨 제거
    hp_label.place_forget()
    mp_label.place_forget()
    energy_label.place_forget()
    coin_label.place_forget()
def store_exit():  # 상점 나간 후
    exitbtn.place_forget()
    canvas.delete("all")
    draw_map()
    draw_item()

root=tkinter.Tk()
root.title("달구지가 불러온 재앙!!(달불재)")
root.resizable(False,False)
root.bind("<KeyPress>",key_press)
root.bind("<KeyRelease>",key_up)
root.bind("<Motion>",mouse_move)
root.bind("<ButtonPress>",mouse_click)
root.bind("<ButtonRelease>",mouse_release)

canvas=tkinter.Canvas(width=1600,height=896)
canvas.pack()

# 맨 처음 화면 설정
start_img=tkinter.PhotoImage(file="start_screen.png")
canvas.create_image(800,448,image=start_img,tag="BG")
startbtn=tkinter.Button(root,text="게임시작",font=("휴먼매직체",40),fg="black",width=8,command=click_startbtn)
endbtn=tkinter.Button(root,text="게임종료",font=("휴먼매직체",40),fg="black",width=8,command=click_endbtn)
startbtn.place(x=690,y=600)
endbtn.place(x=690,y=720)
exitbtn=tkinter.Button(root,text="나가기",font=("휴먼매직체",40),fg="black",command=store_exit)

# 대화용 텍스트 창
left_text=tkinter.Text(width=25,height=6,font=("휴먼매직체",30))
right_text=tkinter.Text(width=25,height=6,font=("휴먼매직체",30))

# 재화 창
hp_label=tkinter.Label(text=f"x {hp}",font=("휴먼매직체",18))
mp_label=tkinter.Label(text=f"x {mp}",font=("휴먼매직체",18))
energy_label=tkinter.Label(text=f"x {energy}",font=("휴먼매직체",18))
coin_label=tkinter.Label(text=f"x {coin}",font=("휴먼매직체",18))

# 스토리 만화 이미지
story=[tkinter.PhotoImage(file="story1.png"),tkinter.PhotoImage(file="story2.png")
       ,tkinter.PhotoImage(file="story3.png"),tkinter.PhotoImage(file="story4.png")
       ,tkinter.PhotoImage(file="story5.png"),tkinter.PhotoImage(file="story6.png")]

# 알림 이미지 (맵 이동 / 상호작용 / next / 커서 / 스킬 설명)
next_img=tkinter.PhotoImage(file="event_next.png")
mapmove_img=tkinter.PhotoImage(file="event_map.png")
chatnpc_img=tkinter.PhotoImage(file="event_npc.png")
cursor_skill=tkinter.PhotoImage(file="cursor_skill.png")
cursor_chr=tkinter.PhotoImage(file="cursor_chr.png")
cursor_item=tkinter.PhotoImage(file="cursor_item.png")
explain_item=[tkinter.PhotoImage(file="ex_hp.png"),tkinter.PhotoImage(file="ex_mp.png"),tkinter.PhotoImage(file="ex_energy.png")]
explain_skill1=[tkinter.PhotoImage(file="attack1.png"),tkinter.PhotoImage(file="attack2.png"),tkinter.PhotoImage(file="attack_run.png")]
explain_skill2=[tkinter.PhotoImage(file="attack3_SH.png"),tkinter.PhotoImage(file="attack3_JM.png"),tkinter.PhotoImage(file="attack3_MS.png"),tkinter.PhotoImage(file="attack3_BC.png")]

# 배경 / 맵 이미지
select_chr=tkinter.PhotoImage(file="select_chr.png")
ChatMap=[tkinter.PhotoImage(file="chat_CU.png"),tkinter.PhotoImage(file="chat_classroom.png"),tkinter.PhotoImage(file="chat_boss.png")]
map_img=[tkinter.PhotoImage(file="map_home.png"),tkinter.PhotoImage(file="map_school.png"),tkinter.PhotoImage(file="map_CU.png"),
         tkinter.PhotoImage(file="map_classroom.png"),tkinter.PhotoImage(file="map_boss.png"),tkinter.PhotoImage(file="map_gameroom.png"),tkinter.PhotoImage(file="map_store.png")]
battle_map=[tkinter.PhotoImage(file="battle_CU.png"),tkinter.PhotoImage(file="battle_classroom.png"),tkinter.PhotoImage(file="battle_boss.png")]
youdie_img=tkinter.PhotoImage(file="game_over.png")
ending_img=tkinter.PhotoImage(file="ending.png")

# 캐립터 이미지 (움직임 / 배틀)
chr_move=[[tkinter.PhotoImage(file="SH_chr_face.png"),tkinter.PhotoImage(file="SH_chr_back.png"),tkinter.PhotoImage(file="SH_chr_left.png"),tkinter.PhotoImage(file="SH_chr_right.png")],
          [tkinter.PhotoImage(file="JM_chr_face.png"),tkinter.PhotoImage(file="JM_chr_back.png"),tkinter.PhotoImage(file="JM_chr_left.png"),tkinter.PhotoImage(file="JM_chr_right.png")],
          [tkinter.PhotoImage(file="MS_chr_face.png"),tkinter.PhotoImage(file="MS_chr_back.png"),tkinter.PhotoImage(file="MS_chr_left.png"),tkinter.PhotoImage(file="MS_chr_right.png")],
          [tkinter.PhotoImage(file="BC_chr_face.png"),tkinter.PhotoImage(file="BC_chr_back.png"),tkinter.PhotoImage(file="BC_chr_left.png"),tkinter.PhotoImage(file="BC_chr_right.png")]]

chr_battle=[tkinter.PhotoImage(file="SH_chr_battle.png"),tkinter.PhotoImage(file="JM_chr_battle.png"),
            tkinter.PhotoImage(file="MS_chr_battle.png"),tkinter.PhotoImage(file="BC_chr_battle.png")]
chr_chat=[tkinter.PhotoImage(file="SH_chr_chat.png"),tkinter.PhotoImage(file="JM_chr_chat.png"),
            tkinter.PhotoImage(file="MS_chr_chat.png"),tkinter.PhotoImage(file="BC_chr_chat.png")]

boss_chr=[[tkinter.PhotoImage(file="boss1.png"),tkinter.PhotoImage(file="boss1_atk.png")],
          [tkinter.PhotoImage(file="boss2.png"),tkinter.PhotoImage(file="boss2_atk.png")],
          [tkinter.PhotoImage(file="boss3.png"),tkinter.PhotoImage(file="boss3_atk.png")]]
boss_chat=[[tkinter.PhotoImage(file="boss1_chat1.png"),tkinter.PhotoImage(file="boss1_chat2.png")],
           [tkinter.PhotoImage(file="boss2_chat1.png"),tkinter.PhotoImage(file="boss2_chat2.png")],
           [tkinter.PhotoImage(file="boss3_chat1.png"),tkinter.PhotoImage(file="boss3_chat2.png")]]

atk_bite=tkinter.PhotoImage(file="atk_bite.png")
atk_scratch=tkinter.PhotoImage(file="atk_scratch.png")
chr_skill=[tkinter.PhotoImage(file="SH_chr_skill.png"),tkinter.PhotoImage(file="JM_chr_skill.png"),
           tkinter.PhotoImage(file="MS_chr_skill.png"),tkinter.PhotoImage(file="BC_chr_skill.png")]
skill_motion=[tkinter.PhotoImage(file="Beam.png"),tkinter.PhotoImage(file="Joke.png"),
              tkinter.PhotoImage(file="Error.png"),tkinter.PhotoImage(file="Throw.png")]
chr_dead=tkinter.PhotoImage(file="surrend.png")

# 캐릭터 객체
character=[GameCharacter("King승헌",200,20,2,"SH_chr_battle.png","ch",250,520,1),
           GameCharacter("Clown지민",150,30,2,"JM_chr_battle.png","ch",250,520,1),
           GameCharacter("Baby민서",170,25,2,"MS_chr_battle.png","ch",250,520,1),
           GameCharacter("Oldest병찬",100,50,2,"BC_chr_battle.png","ch",250,520,1)]
chr_boss=[GameCharacter("학생회",300,10,0,"boss1.png","boss",1400,248,-1),
          GameCharacter("교수님",600,10,0,"boss2.png","boss",1400,248,-1),
          GameCharacter("총장님",1200,10,0,"boss3.png","boss",1400,248,-1)]

play_bgm('bgm1')
root.mainloop()