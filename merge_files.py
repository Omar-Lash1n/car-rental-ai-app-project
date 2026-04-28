import pandas as pd
import os

folder_path = r'F:\Fourth Year\Second Semester\AI Enabled System\Datasets\1' 

df_list = []
all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')] # أو .xlsx

for filename in all_files:
    file_path = os.path.join(folder_path, filename)
    temp_df = pd.read_csv(file_path) 
    
    # استخراج اسم الماركة من اسم الملف مباشرة
    brand_name = filename.split('.')[0]
    
    # إضافة عمود الماركة
    temp_df['brand'] = brand_name
    
    df_list.append(temp_df)
    print(f"✅ تمت إضافة ماركة: {brand_name}")

# دمج كل الملفات
final_df = pd.concat(df_list, ignore_index=True)

# حفظ الملف النهائي
final_df.to_csv('final_clean_cars_dataset.csv', index=False)
print(f"\n🎉 تم الدمج بنجاح! الملف النهائي جاهز بإجمالي عدد صفوف: {len(final_df)}")