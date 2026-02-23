#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# 1) โหลดข้อมูล (offline CSV)
df = pd.read_csv("data/insurance.csv")

# 2) ดูข้อมูลคร่าว ๆ (แนะนำให้รันดู)
print("Shape:", df.shape)
print(df.head())
print(df.dtypes)

# 3) แยก feature (X) และ target (y)
# target คือ charges (ค่าประกัน/ค่ารักษา)
X = df.drop(columns=["charges"])
y = df["charges"]

# 4) แบ่ง train/test (กัน overfit + วัดผลแบบยุติธรรม)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5) ระบุคอลัมน์ที่เป็นตัวเลข vs หมวดหมู่
numeric_features = ["age", "bmi", "children"]
categorical_features = ["sex", "smoker", "region"]

# 6) ตัวแปลงข้อมูล (Preprocessing)
# - ตัวเลข: ใช้ผ่านไปเฉย ๆ (passthrough)
# - หมวดหมู่: OneHotEncoder แปลงเป็น 0/1 หลายคอลัมน์
preprocess = ColumnTransformer(
    transformers=[
        ("num", "passthrough", numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ]
)

# 7) สร้าง Pipeline: preprocess -> model
# Pipeline ช่วยให้ขั้นตอนแปลงข้อมูลและเทรนทำเป็นชุดเดียว ปลอดภัยกว่า
model = Pipeline(
    steps=[
        ("preprocess", preprocess),
        ("regressor", LinearRegression())
    ]
)

# 8) เทรนโมเดล
model.fit(X_train, y_train)

# 9) ทำนายผลบน test set
y_pred = model.predict(X_test)

# 10) ประเมินผล
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("\n=== Linear Regression Results (Insurance) ===")
print(f"MAE : {mae:.2f}")
print(f"MSE : {mse:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R^2 : {r2:.4f}")

# 11) กราฟ: ค่าจริง vs ค่าที่ทำนาย
plt.figure()
plt.scatter(y_test, y_pred)
plt.xlabel("Actual charges")
plt.ylabel("Predicted charges")
plt.title("Actual vs Predicted (Linear Regression)")
plt.show()