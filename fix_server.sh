#!/bin/bash

# سكريبت لإصلاح السطر 838 و 839 مباشرة على السيرفر

FILE="/home/ubuntu/public_html/index-50.html"
BACKUP="/home/ubuntu/public_html/index-50.html.backup_$(date +%Y%m%d_%H%M%S)"

echo "🔄 جاري إصلاح الملف..."

# نسخ احتياطي
cp "$FILE" "$BACKUP"
echo "✅ تم إنشاء نسخة احتياطية: $BACKUP"

# قراءة السطر 838
LINE_838=$(sed -n '838p' "$FILE")

# التحقق إذا كان السطر يحتوي على دالتين
if echo "$LINE_838" | grep -q "function renderNP"; then
    echo "🔧 فصل الدالتين إلى سطرين منفصلين..."
    
    # استبدال السطر 838 بدالة addN فقط
    sed -i '838s/.*/function addN(c,p,type,title,content){var n={type:type||"code",c:c||"",p:p||"",title:title||"",content:content||"",t:new Date()};NL.unshift(n);UN++;var b=document.querySelector(".bnum");if(b){b.textContent=UN;b.classList.add("on");}renderNP();}/' "$FILE"
    
    # إدراج دالة renderNP في سطر جديد بعد 838
    sed -i '838a function renderNP(){var b=document.getElementById("npb");if(!NL.length){b.innerHTML="<div class=\\"np-e\\">لا توجد إشعارات<\/div>";return;}b.innerHTML=NL.slice(0,15).map(function(n){var icon="🔔",color="#22c55e";if(n.type==="code"){icon="🎯";return"<div class=\\"np-i\\"><div style=\\"font-size:0.77rem;font-weight:600;margin-bottom:0.18rem\\">"+icon+" كود ربح جديد<\/div><div class=\\"np-c\\">"+n.c+"<\/div><div style=\\"font-size:0.7rem;color:"+color+"\\">ربح "+n.p+"%<\/div><div style=\\"font-size:0.63rem;color:#8a7a5a;margin-top:0.12rem\\">"+fd(n.t)+"<\/div><\/div>";}else{if(n.type==="success"){icon="✅";color="#22c55e";}else if(n.type==="warning"){icon="⚠️";color="#f0c96a";}else if(n.type==="error"){icon="❌";color="#ef4444";}else{icon="ℹ️";color="#60a5fa";}}return"<div class=\\"np-i\\"><div style=\\"font-size:0.77rem;font-weight:600;margin-bottom:0.18rem;color:"+color+"\\">"+icon+" "+(n.title||"إشعار")+"<\/div><div style=\\"font-size:0.7rem;color:#e2d5b8;line-height:1.5\\">"+(n.content||"")+"<\/div><div style=\\"font-size:0.63rem;color:#8a7a5a;margin-top:0.12rem\\">"+fd(n.t)+"<\/div><\/div>";}}).join("");}' "$FILE"
    
    echo "✅ تم فصل الدالتين"
else
    echo "🔧 إصلاح الاقتباسات في السطر 838..."
    sed -i "838s/'code'/\"code\"/g" "$FILE"
    sed -i "838s/''/\"\"/g" "$FILE"
    sed -i "838s/'.bnum'/\"\.bnum\"/g" "$FILE"
    sed -i "838s/'on'/\"on\"/g" "$FILE"
fi

# إصلاح السطر 839
echo "🔧 إصلاح الاقتباسات في السطر 839..."
sed -i "839s/'npb'/\"npb\"/g" "$FILE"
sed -i "839s/'np-e'/\"np-e\"/g" "$FILE"
sed -i "839s/'np-i'/\"np-i\"/g" "$FILE"
sed -i "839s/'np-c'/\"np-c\"/g" "$FILE"
sed -i "839s/'code'/\"code\"/g" "$FILE"
sed -i "839s/'success'/\"success\"/g" "$FILE"
sed -i "839s/'warning'/\"warning\"/g" "$FILE"
sed -i "839s/'error'/\"error\"/g" "$FILE"
sed -i "839s/'إشعار'/\"إشعار\"/g" "$FILE"

echo "✅ تم إصلاح الملف!"
echo "🔄 قم بإعادة تحميل Apache: systemctl reload apache2"

