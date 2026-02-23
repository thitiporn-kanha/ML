# วิธีสร้างไฟล์ ZIP (ย้ายโปรเจกต์ไปเครื่องใหม่)

ไฟล์นี้อธิบายวิธีการแพ็กโปรเจกต์เป็นไฟล์ .zip อย่างปลอดภัยและ reproducible

สรุปสั้น ๆ
- ใช้สคริปต์ `pack.sh` ที่ root ของ repo เพื่อสร้าง zip โดยอัตโนมัติ
- ดีฟอลต์จะไม่รวม `./.venv`, `results/` และ `.git` (แต่สามารถรวมได้โดย flag)

ตัวอย่างการใช้งาน

1) สร้าง zip ปกติ (exclude .venv และ results):

```bash
./pack.sh
# -> ../ML-project.zip
```

2) กำหนดชื่อไฟล์ output:

```bash
./pack.sh -o ~/Downloads/ml-export.zip
```

3) ถ้าต้องการรวมผลลัพธ์หรือ virtualenv (ไม่แนะนำ สำหรับ sharing):

```bash
./pack.sh --include-results --include-venv
```

หลังแตกไฟล์บนเครื่องใหม่

```bash
unzip ML-project.zip -d ~/projects/ML
cd ~/projects/ML
# สร้าง virtualenv ใหม่
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# ตั้ง permission ให้สคริปต์
chmod +x pack.sh */run_*.sh */main.py

# รัน smoke-test ตัวอย่าง (decision tree)
cd decision_tree
python3 -c "import main; main.main('data/heart.csv','HeartDisease')"
```

หมายเหตุ
- สคริปต์จะพยายามอัปเดต `requirements.txt` โดยใช้ pip ที่อยู่ใน `.venv` ถ้ามี — ถ้าระบบของคุณต้องการ freeze ที่เฉพาะเจาะจงให้รัน `pip freeze > requirements.txt` เองก่อน
- การเก็บ `results/` และไฟล์ binary model ใน Git จะทำให้ repo ใหญ่ขึ้น — ทางที่ดีคือเก็บ model ใน storage ภายนอกหรือใช้ Git LFS
