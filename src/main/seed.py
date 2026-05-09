import random
from main.models import Employee

Employee.objects.all().delete()

unique_ids = random.sample(range(1000, 10000), 50)

Employee.objects.create(
    name="田中 太郎",
    department="開発部",
    email="user01@example.com",
    private_token=f"secret_{unique_ids[0]}"
)

last_names = ["佐藤", "鈴木", "高橋", "田中", "伊藤", "渡辺", "山本", "中村", "小林", "加藤", "吉田", "山田", "佐々木", "山口", "松本"]
first_names = [
    "健", "一郎", "結衣", "淳", "七海", "大輔", "美咲", "拓也", "凛", "翔太",
    "愛", "和也", "陽菜", "直樹", "莉子", "悟", "栞", "慎太郎", "芽衣", "悠人",
    "優子", "太一", "彩花", "康平", "結菜", "亮太", "杏奈", "裕貴", "千夏", "海斗",
    "舞", "健太", "琴音", "雅也", "奏", "隆一", "萌", "雄大", "葵", "俊介",
    "真由", "充", "梨奈", "一輝", "明日香", "哲也", "愛莉", "慶介", "花音", "智也"
]
depts = ["営業部", "開発部", "人事部", "総務部", "マーケティング部", "広報部", "法務部"]
random.shuffle(first_names)

for i in range(1, 50):
    full_name = f"{random.choice(last_names)} {first_names[i-1]}"
    
    token_str = f"secret_{unique_ids[i]}"
    
    Employee.objects.create(
        name=full_name,
        department=random.choice(depts),
        email=f"user{i+1:02d}@example.com",
        private_token=token_str
    )

exit()