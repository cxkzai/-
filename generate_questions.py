from app import app, db
from models import Question
import json
import random
# 题型示例
university_level_questions = [
    
    {
        "question": "找规律：2, 4, 8, 16, ?",
        "options": ["20", "24", "32", "64"],
        "correct_answer": "2",  # 32是正确答案
        "difficulty": 1,
        "type": "logical"
    },
    {
        "question": "找规律：1, 1, 2, 3, 5, ?",
        "options": ["8", "10", "12", "13"],
        "correct_answer": "0",  # 8是正确答案
        "difficulty": 1,
        "type": "logical"
    },
   
    {
        "question": "找规律：3, 9, 27, 81, ?",
        "options": ["162", "243", "324", "405"],
        "correct_answer": "1",  # 243是正确答案
        "difficulty": 1,
        "type": "logical"
    },
    {
        "question": "找规律：1, 4, 9, 16, 25, ?",
        "options": ["30", "36", "40", "45"],
        "correct_answer": "1",  # 36是正确答案
        "difficulty": 1,
        "type": "logical"
    },

    {
        "question": "找规律：1, 2, 4, 8, 16, 32, ?",
        "options": ["64", "128", "256", "512"],
        "correct_answer": "0",  # 64是正确答案
        "difficulty": 1,
        "type": "logical"
    },
    {
        "question": "找规律：2, 3, 5, 7, 11, ?",
        "options": ["13", "14", "15", "16"],
        "correct_answer": "0",  # 13是正确答案
        "difficulty": 1,
        "type": "logical"
    },
       {
        "question": "找规律：1, 2, 4, 8, ?",
        "options": ["10", "12", "14", "16"],
        "correct_answer": "3",  # 16是正确答案
        "difficulty": 1,
        "type": "logical"
    },
    {
        "question": "找规律：3, 6, 12, 24, ?",
        "options": ["36", "48", "60", "72"],
        "correct_answer": "1",  # 48是正确答案
        "difficulty": 1,
        "type": "logical"
    },

    {
        "question": "找规律：2, 5, 10, 17, ?",
        "options": ["26", "30", "34", "40"],
        "correct_answer": "0",  # 26是正确答案
        "difficulty": 1,
        "type": "logical"
    },
    {
        "question": "找规律：1, 1, 2, 3, 5, ?",
        "options": ["8", "10", "12", "13"],
        "correct_answer": "0",  # 8是正确答案
        "difficulty": 1,
        "type": "logical"
    },
 
    {
        "question": "找规律：1, 3, 6, 10, 15, ?",
        "options": ["21", "22", "23", "24"],
        "correct_answer": "0",  # 21是正确答案
        "difficulty": 1,
        "type": "logical"
    },
    {
        "question": "找规律：2, 4, 8, 16, 32, ?",
        "options": ["64", "128", "256", "512"],
        "correct_answer": "0",  # 64是正确答案
        "difficulty": 1,
        "type": "logical"
    },
    {
    "question": "找规律：2, 5, 10, 17, 26,?",
    "options": ["30", "35", "37", "40"],
    "correct_answer": "2",
    "difficulty": 1,
    "type": "logical"
},
{
    "question": "找规律：3, 8, 15, 24, 35,?",
    "options": ["42", "48", "50", "55"],
    "correct_answer": "1",
    "difficulty": 1,
    "type": "logical"
},
{
    "question": "找规律：1, 3, 6, 10, 15,?",
    "options": ["20", "21", "25", "30"],
    "correct_answer": "0",
    "difficulty": 1,
    "type": "logical"
},
{
    "question": "找规律：4, 9, 16, 25, 36,?",
    "options": ["42", "49", "50", "56"],
    "correct_answer": "1",
    "difficulty": 1,
    "type": "logical"
},
{
    "question": "找规律：5, 12, 21, 32, 45,?",
    "options": ["50", "55", "60", "65"],
    "correct_answer": "3",
    "difficulty": 1,
    "type": "logical"
},
{
    "question": "找规律：2, 6, 12, 20, 30,?",
    "options": ["36", "40", "42", "48"],
    "correct_answer": "2",
    "difficulty": 1,
    "type": "logical"
},
{
    "question": "找规律：7, 16, 27, 40, 55,?",
    "options": ["60", "70", "72", "80"],
    "correct_answer": "2",
    "difficulty": 1,
    "type": "logical"
},
{
    "question": "找规律：1, 8, 27, 64, 125,?",
    "options": ["150", "200", "216", "250"],
    "correct_answer": "2",
    "difficulty": 1,
    "type": "logical"
},
{
    "question": "找规律：6, 15, 28, 45, 66,?",
    "options": ["75", "80", "91", "99"],
    "correct_answer": "2",
    "difficulty": 1,
    "type": "logical"
},
{
    "question": "找规律：3, 10, 21, 36, 55,?",
    "options": ["60", "70", "78", "85"],
    "correct_answer": "2",
    "difficulty": 1,
    "type": "logical"
},
{
    "question": "找规律：8, 19, 34, 53, 76,?",
    "options": ["85", "90", "100", "103"],
    "correct_answer": "3",
    "difficulty": 1,
    "type": "logical"
},
{
    "question": "找规律：11, 22, 37, 56, 79,?",
    "options": ["90", "100", "106", "110"],
    "correct_answer": "2",
    "difficulty": 1,
    "type": "logical"
},
{
    "question": "找规律：4, 13, 28, 49, 76,?",
    "options": ["85", "90", "100", "109"],
    "correct_answer": "3",
    "difficulty": 1,
    "type": "logical"
},
{
    "question": "找规律：9, 20, 37, 60, 89,?",
    "options": ["100", "110", "120", "124"],
    "correct_answer": "3",
    "difficulty": 1,
    "type": "logical"
},
{
    "question": "找规律：5, 14, 31, 56, 89,?",
    "options": ["100", "110", "125", "130"],
    "correct_answer": "2",
    "difficulty": 1,
    "type": "logical"
},
{
    "question": "找规律：12, 27, 48, 75, 108,?",
    "options": ["120", "135", "140", "150"],
    "correct_answer": "1",
    "difficulty": 1,
    "type": "logical"
},
{
    "question": "找规律：7, 18, 35, 58, 87,?",
    "options": ["100", "110", "122", "130"],
    "correct_answer": "2",
    "difficulty": 1,
    "type": "logical"
},
{
    "question": "找规律：10, 23, 42, 67, 98,?",
    "options": ["110", "125", "130", "135"],
    "correct_answer": "3",
    "difficulty": 1,
    "type": "logical"
},
{
    "question": "找规律：13, 28, 49, 76, 109,?",
    "options": ["120", "135", "140", "150"],
    "correct_answer": "2",
    "difficulty": 1,
    "type": "logical"
},
{
    "question": "找规律：6, 17, 34, 57, 86,?",
    "options": ["100", "110", "121", "130"],
    "correct_answer": "2",
    "difficulty": 1,
    "type": "logical"
},
    {
        "question": "折纸题：将一张纸对折两次，打一个洞，展开后会看到几个洞？",
        "options": ["2个", "3个", "4个", "6个"],
        "correct_answer": "2",
        "difficulty": 2,
        "type": "spatial"
    },
    {
        "question": "一个立方体展开后可能的形状是？",
        "options": ["十字形", "T形", "L形", "以上都可能"],
        "correct_answer": "3",
        "difficulty": 2,
        "type": "spatial"
    },
    {
        "question": "从正面看是圆形，从侧面看是矩形的物体可能是？",
        "options": ["球体", "圆柱体", "圆锥体", "立方体"],
        "correct_answer": "1",
        "difficulty": 2,
        "type": "spatial"
    },
    {
        "question": "将一个正方体沿对角线切开，截面的形状是？",
        "options": ["正方形", "长方形", "三角形", "不规则四边形"],
        "correct_answer": "2",
        "difficulty": 2,
        "type": "spatial"
    },
      {
        "question": "如果所有的A都是B，所有的B都是C，那么：",
        "options": [
            "所有的A都是C",
            "部分A是C",
            "没有A是C",
            "无法确定"
        ],
        "correct_answer": "0",
        "difficulty": 2,
        "type": "logical"
    },
    {
        "question": "找规律：1, 3, 6, 10, ?",
        "options": ["15", "14", "16", "13"],
        "correct_answer": "0",  # 15是正确答案
        "difficulty": 1,
        "type": "logical"
    },
    {
        "question": "在一个家庭中，有两对父子和三个人，这可能吗？",
        "options": ["不可能", "可能，爷爷-父亲-儿子", "可能，两对双胞胎", "数据不足"],
        "correct_answer": "1",
        "difficulty": 2,
        "type": "logical"
    },
    {
        "question": "小明比小红大，小红比小华大，那么：",
        "options": ["小明一定比小华大", "小明可能比小华小", "无法确定", "以上都不对"],
        "correct_answer": "0",
        "difficulty": 2,
        "type": "logical"
    },
    {
    "question": "如果所有的猫都是哺乳动物，所有的哺乳动物都是脊椎动物，那么：",
    "options": [
        "所有的猫都是脊椎动物",
        "部分猫是脊椎动物",
        "没有猫是脊椎动物",
        "无法确定"
    ],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "logical"
},
{
    "question": "从正面看是正方形，从上面看也是正方形的物体可能是？",
    "options": ["长方体", "正方体", "三棱柱", "圆柱体"],
    "correct_answer": "1",
    "difficulty": 2,
    "type": "spatial"
},
{
    "question": "从正面看是三角形，从侧面看也是三角形的物体可能是？",
    "options": ["三棱柱", "三棱锥", "圆锥体", "球体"],
    "correct_answer": "1",
    "difficulty": 2,
    "type": "spatial"
},
{
    "question": "从正面看是矩形，从上面看是圆形的物体可能是？",
    "options": ["圆柱体", "长方体", "圆锥体", "三棱柱"],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "spatial"
},
{
    "question": "从正面看是梯形，从侧面看是矩形的物体可能是？",
    "options": ["四棱台", "三棱柱", "圆锥体", "球体"],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "spatial"
},
{
    "question": "从正面看是菱形，从上面看也是菱形的物体可能是？",
    "options": ["菱柱体", "正方体", "三棱柱", "圆柱体"],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "spatial"
},
{
    "question": "从正面看是长方形，从侧面看是三角形的物体可能是？",
    "options": ["三棱柱", "长方体", "圆锥体", "球体"],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "spatial"
},
{
    "question": "从正面看是正六边形，从上面看也是正六边形的物体可能是？",
    "options": ["六棱柱", "正方体", "三棱柱", "圆柱体"],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "spatial"
},
{
    "question": "从正面看是等腰三角形，从侧面看是等腰三角形的物体可能是？",
    "options": ["三棱锥", "圆锥体", "三棱柱", "球体"],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "spatial"
},
{
    "question": "从正面看是半圆形，从侧面看是矩形的物体可能是？",
    "options": ["半圆柱体", "圆锥体", "三棱柱", "球体"],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "spatial"
},
{
    "question": "从正面看是五边形，从上面看也是五边形的物体可能是？",
    "options": ["五棱柱", "正方体", "三棱柱", "圆柱体"],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "spatial"
},
{
    "question": "从正面看是L形，从侧面看是矩形的物体可能是？",
    "options": ["特殊组合体", "三棱柱", "圆锥体", "球体"],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "spatial"
},
{
    "question": "从正面看是十字形，从侧面看是矩形的物体可能是？",
    "options": ["特殊组合体", "三棱柱", "圆锥体", "球体"],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "spatial"
},
{
    "question": "从正面看是圆形，从上面看是十字形的物体可能是？",
    "options": ["特殊组合体", "圆柱体", "圆锥体", "球体"],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "spatial"
},
{
    "question": "从正面看是三角形，从上面看是圆形的物体可能是？",
    "options": ["特殊组合体", "三棱锥", "圆锥体", "球体"],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "spatial"
},
{
    "question": "从正面看是矩形，从侧面看是梯形的物体可能是？",
    "options": ["四棱台", "长方体", "圆锥体", "球体"],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "spatial"
},
{
    "question": "从正面看是正八边形，从上面看也是正八边形的物体可能是？",
    "options": ["八棱柱", "正方体", "三棱柱", "圆柱体"],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "spatial"
},
{
    "question": "从正面看是不规则四边形，从侧面看是矩形的物体可能是？",
    "options": ["特殊组合体", "三棱柱", "圆锥体", "球体"],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "spatial"
},
{
    "question": "从正面看是扇形，从侧面看是三角形的物体可能是？",
    "options": ["圆锥体", "三棱锥", "三棱柱", "球体"],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "spatial"
},
{
    "question": "从正面看是椭圆，从侧面看是矩形的物体可能是？",
    "options": ["椭圆柱体", "长方体", "圆锥体", "球体"],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "spatial"
},
{
    "question": "从正面看是六边形，从侧面看是矩形的物体可能是？",
    "options": ["六棱柱", "长方体", "圆锥体", "球体"],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "spatial"
},
{
    "question": "如果所有的正方形都是矩形，所有的矩形都是四边形，那么：",
    "options": [
        "所有的正方形都是四边形",
        "部分正方形是四边形",
        "没有正方形是四边形",
        "无法确定"
    ],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "logical"
},
{
    "question": "如果所有的玫瑰都是花，所有的花都是植物，那么：",
    "options": [
        "所有的玫瑰都是植物",
        "部分玫瑰是植物",
        "没有玫瑰是植物",
        "无法确定"
    ],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "logical"
},
{
    "question": "如果所有的大学生都是学生，所有的学生都是受教育者，那么：",
    "options": [
        "所有的大学生都是受教育者",
        "部分大学生是受教育者",
        "没有大学生是受教育者",
        "无法确定"
    ],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "logical"
},
{
    "question": "如果所有的偶数都是整数，所有的整数都是有理数，那么：",
    "options": [
        "所有的偶数都是有理数",
        "部分偶数是有理数",
        "没有偶数是有理数",
        "无法确定"
    ],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "logical"
},
{
    "question": "如果所有的铅笔都是文具，所有的文具都是用品，那么：",
    "options": [
        "所有的铅笔都是用品",
        "部分铅笔是用品",
        "没有铅笔是用品",
        "无法确定"
    ],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "logical"
},
{
    "question": "如果所有的汽车都是交通工具，所有的交通工具都是工具，那么：",
    "options": [
        "所有的汽车都是工具",
        "部分汽车是工具",
        "没有汽车是工具",
        "无法确定"
    ],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "logical"
},
{
    "question": "如果所有的医生都是职业者，所有的职业者都是社会成员，那么：",
    "options": [
        "所有的医生都是社会成员",
        "部分医生是社会成员",
        "没有医生是社会成员",
        "无法确定"
    ],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "logical"
},
{
    "question": "如果所有的锐角都是角，所有的角都是几何图形，那么：",
    "options": [
        "所有的锐角都是几何图形",
        "部分锐角是几何图形",
        "没有锐角是几何图形",
        "无法确定"
    ],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "logical"
},
{
    "question": "如果所有的小说都是文学作品，所有的文学作品都是作品，那么：",
    "options": [
        "所有的小说都是作品",
        "部分小说是作品",
        "没有小说是作品",
        "无法确定"
    ],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "logical"
},
{
    "question": "如果所有的篮球都是球类，所有的球类都是体育器材，那么：",
    "options": [
        "所有的篮球都是体育器材",
        "部分篮球是体育器材",
        "没有篮球是体育器材",
        "无法确定"
    ],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "logical"
},
{
    "question": "如果所有的手表都是计时工具，所有的计时工具都是工具，那么：",
    "options": [
        "所有的手表都是工具",
        "部分手表是工具",
        "没有手表是工具",
        "无法确定"
    ],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "logical"
},
{
    "question": "如果所有的鸟类都是动物，所有的动物都是生物，那么：",
    "options": [
        "所有的鸟类都是生物",
        "部分鸟类是生物",
        "没有鸟类是生物",
        "无法确定"
    ],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "logical"
},
{
    "question": "如果所有的红色物体都是有颜色的物体，所有有颜色的物体都是物体，那么：",
    "options": [
        "所有的红色物体都是物体",
        "部分红色物体是物体",
        "没有红色物体是物体",
        "无法确定"
    ],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "logical"
},
{
    "question": "如果所有的质数都是自然数，所有的自然数都是数，那么：",
    "options": [
        "所有的质数都是数",
        "部分质数是数",
        "没有质数是数",
        "无法确定"
    ],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "logical"
},
{
    "question": "如果所有的椅子都是家具，所有的家具都是生活用品，那么：",
    "options": [
        "所有的椅子都是生活用品",
        "部分椅子是生活用品",
        "没有椅子是生活用品",
        "无法确定"
    ],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "logical"
},
{
    "question": "如果所有的山峰都是地形，所有的地形都是地理事物，那么：",
    "options": [
        "所有的山峰都是地理事物",
        "部分山峰是地理事物",
        "没有山峰是地理事物",
        "无法确定"
    ],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "logical"
},
{
    "question": "如果所有的演员都是艺人，所有的艺人都是职业人员，那么：",
    "options": [
        "所有的演员都是职业人员",
        "部分演员是职业人员",
        "没有演员是职业人员",
        "无法确定"
    ],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "logical"
},
{
    "question": "如果所有的智能手机都是电子设备，所有的电子设备都是设备，那么：",
    "options": [
        "所有的智能手机都是设备",
        "部分智能手机是设备",
        "没有智能手机是设备",
        "无法确定"
    ],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "logical"
},
{
    "question": "如果所有的湖泊都是水域，所有的水域都是地理环境的一部分，那么：",
    "options": [
        "所有的湖泊都是地理环境的一部分",
        "部分湖泊是地理环境的一部分",
        "没有湖泊是地理环境的一部分",
        "无法确定"
    ],
    "correct_answer": "0",
    "difficulty": 2,
    "type": "logical"
},
    {
    "question": "一个三棱柱展开后的形状是？",
    "options": ["长方形与两个三角形相连", "三个长方形相连", "四个三角形相连", "以上都有可能"],
    "correct_answer": "3",
    "difficulty": 3,
    "type": "logical"
    },
{
    "question": "一个圆柱展开后的形状是？",
    "options": ["两个圆形和一个长方形", "一个圆形和一个长方形", "两个长方形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个圆锥展开后的形状是？",
    "options": ["一个圆形和一个扇形", "一个三角形", "一个梯形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个正四面体展开后的形状是？",
    "options": ["四个三角形相连成菱形", "三个三角形相连", "两个三角形重叠和两个三角形相连", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个长方体（特殊的，有两个面是正方形）展开后的形状是？",
    "options": ["四个长方形和两个正方形", "六个长方形", "三个正方形和三个长方形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个三棱锥展开后的形状是？",
    "options": ["三个三角形相连和一个独立三角形", "四个三角形相连", "两个三角形重叠和两个三角形相连", "以上都有可能"],
    "correct_answer": "1",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个五棱柱展开后的形状是？",
    "options": ["五个长方形和两个五边形", "七个长方形", "四个长方形和三个五边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个六面体（正方体是特殊六面体）展开后的形状是？",
    "options": ["六个正方形相连成十字形", "四个正方形相连成T形和两个正方形", "三个正方形相连成L形和三个正方形", "以上都有可能"],
    "correct_answer": "3",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个四棱锥展开后的形状是？",
    "options": ["四个三角形和一个四边形", "五个三角形", "三个三角形和两个四边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个八面体展开后的形状是？",
    "options": ["八个三角形相连成八角形", "六个三角形和两个四边形", "四个三角形和四个四边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个七棱柱展开后的形状是？",
    "options": ["七个长方形和两个七边形", "九个长方形", "六个长方形和三个七边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个十面体展开后的形状是？",
    "options": ["十个三角形相连", "八个三角形和两个四边形", "六个三角形和四个四边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个九棱柱展开后的形状是？",
    "options": ["九个长方形和两个九边形", "十一个长方形", "八个长方形和三个九边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个三棱柱（底面是等边三角形）展开后的形状是？",
    "options": ["三个相同的长方形和两个等边三角形", "两个相同的长方形和三个等边三角形", "四个长方形和一个等边三角形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个圆柱（侧面沿高剪开）展开后的形状是？",
    "options": ["长方形", "正方形（底面周长和高相等时）", "平行四边形（斜着剪开）", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个圆锥（侧面沿母线剪开）展开后的形状是？",
    "options": ["扇形", "半圆形（底面直径和母线相等时）", "大于半圆的扇形（底面直径小于母线）", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个正六棱柱展开后的形状是？",
    "options": ["六个长方形和两个正六边形", "八个长方形", "四个长方形和四个正六边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个正八棱柱展开后的形状是？",
    "options": ["八个长方形和两个正八边形", "十个长方形", "六个长方形和四个正八边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个正十棱柱展开后的形状是？",
    "options": ["十个长方形和两个正十边形", "十二个长方形", "八个长方形和四个正十边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个五棱锥展开后的形状是？",
    "options": ["五个三角形和一个五边形", "六个三角形", "四个三角形和两个五边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个六棱锥展开后的形状是？",
    "options": ["六个三角形和一个六边形", "七个三角形", "五个三角形和两个六边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个七棱锥展开后的形状是？",
    "options": ["七个三角形和一个七边形", "八个三角形", "六个三角形和两个七边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个八棱锥展开后的形状是？",
    "options": ["八个三角形和一个八边形", "九个三角形", "七个三角形和两个八边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个九棱锥展开后的形状是？",
    "options": ["九个三角形和一个九边形", "十个三角形", "八个三角形和两个九边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个十棱锥展开后的形状是？",
    "options": ["十个三角形和一个十边形", "十一个三角形", "九个三角形和两个十边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个三棱柱（底面是直角三角形）展开后的形状是？",
    "options": ["三个长方形和两个直角三角形", "两个长方形和三个直角三角形", "四个长方形和一个直角三角形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个圆柱（侧面不沿高剪开）展开后的形状是？",
    "options": ["平行四边形", "不规则四边形", "梯形（特殊情况）", "以上都有可能"],
    "correct_answer": "3",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个圆锥（侧面不沿母线剪开）展开后的形状是？",
    "options": ["不规则扇形", "部分扇形和部分三角形", "类似椭圆的扇形（特殊情况）", "以上都有可能"],
    "correct_answer": "3",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个正十二棱柱展开后的形状是？",
    "options": ["十二个长方形和两个正十二边形", "十四个长方形", "十个长方形和四个正十二边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个正十四棱柱展开后的形状是？",
    "options": ["十四个长方形和两个正十四边形", "十六个长方形", "十二个长方形和四个正十四边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个正十六棱柱展开后的形状是？",
    "options": ["十六个长方形和两个正十六边形", "十八个长方形", "十四个长方形和四个正十六边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个正二十棱柱展开后的形状是？",
    "options": ["二十个长方形和两个正二十边形", "二十二个长方形", "十八个长方形和四个正二十边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个三棱柱（底面是等腰三角形）展开后的形状是？",
    "options": ["三个长方形和两个等腰三角形", "两个长方形和三个等腰三角形", "四个长方形和一个等腰三角形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个圆柱（底面周长是高的2倍）展开后的形状是？",
    "options": ["长方形（长是宽的2倍）", "正方形（特殊情况）", "平行四边形（斜着看）", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个圆锥（底面半径和母线比为1:3）展开后的形状是？",
    "options": ["扇形（圆心角为120°）", "扇形（圆心角为60°）", "扇形（圆心角为90°）", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个正十三棱柱展开后的形状是？",
    "options": ["十三个长方形和两个正十三边形", "十五个长方形", "十一个长方形和四个正十三边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个正十五棱柱展开后的形状是？",
    "options": ["十五个长方形和两个正十五边形", "十七个长方形", "十三个长方形和四个正十五边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个正十七棱柱展开后的形状是？",
    "options": ["十七个长方形和两个正十七边形", "十九个长方形", "十五个长方形和四个正十七边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个正十九棱柱展开后的形状是？",
    "options": ["十九个长方形和两个正十九边形", "二十一个长方形", "十七个长方形和四个正十九边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个三棱柱（底面三角形三条边不相等）展开后的形状是？",
    "options": ["三个长方形和两个不等边三角形", "两个长方形和三个不等边三角形", "四个长方形和一个不等边三角形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个圆柱（底面周长是高的3倍）展开后的形状是？",
    "options": ["长方形（长是宽的3倍）", "正方形（特殊情况，斜着看近似）", "平行四边形（斜剪）", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个圆锥（底面半径和母线比为1:4）展开后的形状是？",
    "options": ["扇形（圆心角为90°）", "扇形（圆心角为45°）", "扇形（圆心角为60°）", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个正十八棱柱展开后的形状是？",
    "options": ["十八个长方形和两个正十八边形", "二十个长方形", "十六个长方形和四个正十八边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个正二十一棱柱展开后的形状是？",
    "options": ["二十一个长方形和两个正二十一边形", "二十三个长方形", "十九个长方形和四个正二十一边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个正二十二棱柱展开后的形状是？",
    "options": ["二十二个长方形和两个正二十二边形", "二十四个长方形", "二十个长方形和四个正二十二边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个正二十三棱柱展开后的形状是？",
    "options": ["二十三个长方形和两个正二十三边形", "二十五个长方形", "二十一个长方形和四个正二十三边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个正二十四棱柱展开后的形状是？",
    "options": ["二十四个长方形和两个正二十四边形", "二十六个长方形", "二十二个长方形和四个正二十四边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个正二十五棱柱展开后的形状是？",
    "options": ["二十五个长方形和两个正二十五边形", "二十七个长方形", "二十三个长方形和四个正二十五边形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
},
{
    "question": "一个三棱柱（底面三角形有一个角为60°）展开后的形状是？",
    "options": ["三个长方形和两个有60°角的三角形", "两个长方形和三个有60°角的三角形", "四个长方形和一个有60°角的三角形", "以上都有可能"],
    "correct_answer": "0",
    "difficulty": 3,
    "type": "logical"
}
]

def generate_questions():
    with app.app_context():
        # 清空现有题目
        Question.query.delete()
        
        # 直接使用 university_level_questions 中的题目
        for question in university_level_questions:
            question_data = {
                "options": question['options'],
                "correct_index": int(question['correct_answer']),
                "content": question['question']
            }
            
            db_question = Question(
                question_type=question['type'],
                difficulty=question['difficulty'],
                question_data=json.dumps(question_data)
            )
            db.session.add(db_question)
        
        # 提交到数据库
        db.session.commit()
        print(f"题目导入完成！共导入 {len(university_level_questions)} 道题目")

if __name__ == "__main__":
    generate_questions()
