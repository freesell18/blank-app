import json

# ==========================================
# 1. 數據定義：風味矩陣 (Flavor Matrix)
# ==========================================

# 中菜數據庫：定義油脂、鮮味、辛辣、鹹度
food_db = {
    "燒賣": {"fat": 4, "umami": 4, "spicy": 1, "salt": 3, "desc": "豬肉油脂豐富，蝦仁帶鮮味"},
    "紅燒鮑魚": {"fat": 2, "umami": 5, "spicy": 1, "salt": 4, "desc": "極高鮮味，醬汁濃郁黏稠"},
    "避風塘炒蟹": {"fat": 4, "umami": 4, "spicy": 4, "salt": 4, "desc": "蒜香重，辛辣且油炸"},
}

# 酒類數據庫：定義酸度、單寧、酒體、甜度，以及存放位置
wine_db = {
    "德國雷司令白葡萄酒": {
        "acidity": 5, "tannin": 1, "body": 2, "sweetness": 2, 
        "location": "Shelf-A-01", "stock": 12, "style": "高酸、果香"
    },
    "波爾多紅葡萄酒": {
        "acidity": 3, "tannin": 5, "body": 5, "sweetness": 1, 
        "location": "Shelf-B-05", "stock": 6, "style": "重單寧、木桶味"
    },
    "純米吟釀清酒": {
        "acidity": 2, "tannin": 1, "body": 3, "sweetness": 3, 
        "location": "Fridge-01", "stock": 8, "style": "旨味(Umami)豐富、米香"
    }
}

# ==========================================
# 2. 配對邏輯引擎 (The Sommelier Logic)
# ==========================================

def calculate_pairing_score(food_attr, wine_attr):
    """
    這裡模擬侍酒師的配對原則：
    1. 高油脂食物 (Food Fat) 需要 高酸度酒 (Wine Acidity) 來解膩。
    2. 高鮮味食物 (Food Umami) 遇到 高單寧 (Wine Tannin) 會變苦 (負分)。
    3. 辛辣食物 (Food Spicy) 適合 有甜度 (Wine Sweetness) 的酒。
    """
    score = 50  # 基礎分
    
    # 原則 1: 酸度化解油脂 (Acidity cuts Fat)
    if food_attr['fat'] >= 4 and wine_attr['acidity'] >= 4:
        score += 20
    
    # 原則 2: 鮮味避開單寧 (Umami vs Tannin Clash)
    if food_attr['umami'] >= 4 and wine_attr['tannin'] >= 4:
        score -= 30
    
    # 原則 3: 旨味互補 (Umami Synergy)
    if food_attr['umami'] >= 4 and wine_attr.get('sweetness', 0) >= 3:
        score += 15
        
    return score

# ==========================================
# 3. 核心功能：搜尋與建議
# ==========================================

def get_recommendation(target_food_name):
    if target_food_name not in food_db:
        return "找不到該菜色數據。"

    food = food_db[target_food_name]
    results = []

    for wine_name, wine in wine_db.items():
        score = calculate_pairing_score(food, wine)
        results.append({
            "wine": wine_name,
            "score": score,
            "location": wine['location'],
            "style": wine['style']
        })

    # 按分數從高到低排序
    results.sort(key=lambda x: x['score'], reverse=True)
    return results

# ==========================================
# 4. 模擬 AI 輸出 (結合 RAG 概念)
# ==========================================

def simulate_ai_response(food_name, best_match):
    """
    模擬將數據傳給 Gemini 後生成的專業人話回覆
    """
    prompt_context = f"菜色：{food_name} ({food_db[food_name]['desc']})"
    pairing_logic = f"推薦：{best_match['wine']}。理由：該酒屬性為{best_match['style']}。"
    
    print(f"--- 🍷 AI 侍酒師建議 ---")
    print(f"【用餐情境】您正在享用：{food_name}")
    print(f"【最佳推薦】{best_match['wine']}")
    print(f"【推薦理由】{food_name}口感較為{food_db[food_name]['desc']}，")
    print(f"匹配到這款酒，其{best_match['style']}能完美平衡口感。")
    print(f"【酒窖指引】請前往：{best_match['location']} 取酒。")
    print(f"------------------------")

# ==========================================
# 5. 執行示範
# ==========================================

# 範例一：搜尋燒賣的配酒
print("用戶查詢：燒賣應該配什麼酒？\n")
recommendations = get_recommendation("燒賣")
simulate_ai_response("燒賣", recommendations[0])

print("\n")

# 範例二：搜尋紅燒鮑魚的配酒
print("用戶查詢：紅燒鮑魚應該配什麼酒？\n")
recommendations = get_recommendation("紅燒鮑魚")
simulate_ai_response("紅燒鮑魚", recommendations[0])
