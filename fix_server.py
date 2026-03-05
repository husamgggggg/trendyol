#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت لإصلاح السطر 838 و 839 في index-50.html على السيرفر
"""

import re
import shutil
from datetime import datetime

FILE_PATH = "/home/ubuntu/public_html/index-50.html"
BACKUP_PATH = f"/home/ubuntu/public_html/index-50.html.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# قراءة الملف
with open(FILE_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# نسخ احتياطي
shutil.copy2(FILE_PATH, BACKUP_PATH)
print(f"✅ تم إنشاء نسخة احتياطية: {BACKUP_PATH}")

# إصلاح السطر 838
if len(lines) >= 838:
    line_838 = lines[837]  # index 837 = line 838
    
    # إذا كان السطر يحتوي على دالتين، فصلها
    if 'function renderNP' in line_838 and 'function addN' in line_838:
        # استبدال السطر 838 بدالة addN فقط
        lines[837] = 'function addN(c,p,type,title,content){var n={type:type||"code",c:c||"",p:p||"",title:title||"",content:content||"",t:new Date()};NL.unshift(n);UN++;var b=document.querySelector(".bnum");if(b){b.textContent=UN;b.classList.add("on");}renderNP();}\n'
        
        # إدراج دالة renderNP في سطر جديد
        rendernp_line = 'function renderNP(){var b=document.getElementById("npb");if(!NL.length){b.innerHTML="<div class=\\"np-e\\">لا توجد إشعارات</div>";return;}b.innerHTML=NL.slice(0,15).map(function(n){var icon="🔔",color="#22c55e";if(n.type==="code"){icon="🎯";return"<div class=\\"np-i\\"><div style=\\"font-size:0.77rem;font-weight:600;margin-bottom:0.18rem\\">"+icon+" كود ربح جديد</div><div class=\\"np-c\\">"+n.c+"</div><div style=\\"font-size:0.7rem;color:"+color+"\\">ربح "+n.p+"%</div><div style=\\"font-size:0.63rem;color:#8a7a5a;margin-top:0.12rem\\">"+fd(n.t)+"</div></div>";}else{if(n.type==="success"){icon="✅";color="#22c55e";}else if(n.type==="warning"){icon="⚠️";color="#f0c96a";}else if(n.type==="error"){icon="❌";color="#ef4444";}else{icon="ℹ️";color="#60a5fa";}}return"<div class=\\"np-i\\"><div style=\\"font-size:0.77rem;font-weight:600;margin-bottom:0.18rem;color:"+color+"\\">"+icon+" "+(n.title||"إشعار")+"</div><div style=\\"font-size:0.7rem;color:#e2d5b8;line-height:1.5\\">"+(n.content||"")+"</div><div style=\\"font-size:0.63rem;color:#8a7a5a;margin-top:0.12rem\\">"+fd(n.t)+"</div></div>";}}).join("");}\n'
        lines.insert(838, rendernp_line)
        print("✅ تم فصل الدالتين إلى سطرين منفصلين")
    else:
        # إصلاح الاقتباسات في السطر 838
        lines[837] = re.sub(r"'code'", '"code"', lines[837])
        lines[837] = re.sub(r"''", '""', lines[837])
        lines[837] = re.sub(r"'\.bnum'", '".bnum"', lines[837])
        lines[837] = re.sub(r"'on'", '"on"', lines[837])
        print("✅ تم إصلاح الاقتباسات في السطر 838")

# إصلاح السطر 839
if len(lines) >= 839:
    line_839 = lines[838]  # index 838 = line 839
    
    # استبدال جميع الاقتباسات المفردة بثنائية
    fixed_line = line_839
    fixed_line = re.sub(r"'npb'", '"npb"', fixed_line)
    fixed_line = re.sub(r"'np-e'", '"np-e"', fixed_line)
    fixed_line = re.sub(r"'np-i'", '"np-i"', fixed_line)
    fixed_line = re.sub(r"'np-c'", '"np-c"', fixed_line)
    fixed_line = re.sub(r"'code'", '"code"', fixed_line)
    fixed_line = re.sub(r"'success'", '"success"', fixed_line)
    fixed_line = re.sub(r"'warning'", '"warning"', fixed_line)
    fixed_line = re.sub(r"'error'", '"error"', fixed_line)
    fixed_line = re.sub(r"'إشعار'", '"إشعار"', fixed_line)
    
    # استبدال الاقتباسات المفردة في السلاسل النصية
    fixed_line = re.sub(r"='([^']*)'", r'="\1"', fixed_line)
    
    lines[838] = fixed_line
    print("✅ تم إصلاح الاقتباسات في السطر 839")

# كتابة الملف
with open(FILE_PATH, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"✅ تم إصلاح الملف: {FILE_PATH}")
print("🔄 قم بإعادة تحميل Apache: systemctl reload apache2")

