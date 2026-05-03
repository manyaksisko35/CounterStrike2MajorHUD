from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

canli_mac_verisi = {
    "t_skor": 0, "ct_skor": 0, "round": 0,
    "bomba_durumu": "", "faz": "", "sure": 0.0,
    "t_takimi": [], "ct_takimi": [],
    "aktif_oyuncu": None
}

@app.route('/', methods=['GET', 'POST'])
def gsi_dinle():
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            if not data: return "No Data", 400

            map_data = data.get("map") or {}
            canli_mac_verisi["t_skor"] = map_data.get("team_t", {}).get("score", 0)
            canli_mac_verisi["ct_skor"] = map_data.get("team_ct", {}).get("score", 0)
            canli_mac_verisi["round"] = map_data.get("round", 0)

            round_data = data.get("round") or {}
            canli_mac_verisi["bomba_durumu"] = round_data.get("bomb", "")
            
            phase_data = data.get("phase_countdowns") or {}
            canli_mac_verisi["faz"] = phase_data.get("phase", "")
            canli_mac_verisi["sure"] = float(phase_data.get("phase_ends_in", "0.0"))

            t_liste = []
            ct_liste = []
            allplayers = data.get("allplayers") or {}
            
            for steamid, p in allplayers.items():
                ana_silah = ""
                bombalar = []
                weapons = p.get("weapons") or {}
                
                for w_id, w_info in weapons.items():
                    w_type = w_info.get("type", "")
                    w_name = w_info.get("name", "").replace("weapon_", "")
                    if w_type == "Grenade":
                        bombalar.append(w_name)
                    elif w_type not in ["Knife", "C4", "Pistol"]:
                        ana_silah = w_name
                
                if not ana_silah:
                    for w_id, w_info in weapons.items():
                        if w_info.get("type") == "Pistol":
                            ana_silah = w_info.get("name", "").replace("weapon_", "")

                state = p.get("state") or {}
                stats = p.get("match_stats") or {}
                
                oyuncu = {
                    "isim": p.get("name", "Bilinmiyor"),
                    "hp": state.get("health", 0),
                    "para": state.get("money", 0),
                    "kill": stats.get("kills", 0),
                    "olum": stats.get("deaths", 0),
                    "silah": ana_silah.upper(),
                    "bombalar": bombalar
                }
                if p.get("team") == "T":
                    t_liste.append(oyuncu)
                elif p.get("team") == "CT":
                    ct_liste.append(oyuncu)
                    
            canli_mac_verisi["t_takimi"] = t_liste
            canli_mac_verisi["ct_takimi"] = ct_liste


            p_obs = data.get("player") or {}
            if p_obs and p_obs.get("team") in ["T", "CT"]:
                mermi = 0
                mermi_yedek = 0
                obs_weapons = p_obs.get("weapons") or {}
                for w_id, w_info in obs_weapons.items():
                    if w_info.get("state") == "active":
                        mermi = w_info.get("ammo_clip", 0)
                        mermi_yedek = w_info.get("ammo_reserve", 0)

                obs_state = p_obs.get("state") or {}
                obs_stats = p_obs.get("match_stats") or {}
                
                canli_mac_verisi["aktif_oyuncu"] = {
                    "isim": p_obs.get("name", ""),
                    "takim": p_obs.get("team", ""),
                    "hp": obs_state.get("health", 0),
                    "zirt": obs_state.get("armor", 0),
                    "mermi": mermi,
                    "mermi_yedek": mermi_yedek,
                    "kill": obs_stats.get("kills", 0),
                    "asist": obs_stats.get("assists", 0),
                    "olum": obs_stats.get("deaths", 0)
                }
            else:
                canli_mac_verisi["aktif_oyuncu"] = None

            return "OK", 200
        except Exception as e:
            return "Hata Atlandi", 200
    else:
        return "CS2 GSI Sunucusu Aktif", 200

@app.route('/canli_veri', methods=['GET'])
def veri_yolla():
    return jsonify(canli_mac_verisi), 200

if __name__ == '__main__':
    app.run(port=3000, host='0.0.0.0')