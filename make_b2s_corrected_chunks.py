import csv, os
base_onedrive = r'C:\Users\tbank\OneDrive\NOLO Video Scheduling\Current Project\Brand2Social Upload Chunks\7PM_2026-06-02_Corrected_Metadata'
base_allowed = r'C:\Users\tbank\Desktop\Live Cowork\b2s_corrected_upload_chunks'
os.makedirs(base_onedrive, exist_ok=True)
os.makedirs(base_allowed, exist_ok=True)
header = ['Schedule No','Schedule Date/Time(DD/MM/YYYY HH:mm:ss)','Common Description','Common First Comment','Is Draft','Need Approval','Errors','Connected Profile Id','Connected Profile Name','Social Media','Description','First Comment','Post Type','Youtube Privacy','Youtube Title','Youtube Thumbnail','Pinterest Title','Pinterest Boards','Pinterest Board Sections','Pinterest Link','Pinterest Cover Image','Gbusiness Button Type','Gbusiness Url','Gbusiness Title','Gbusiness Start Date','Gbusiness End Date','Gbusiness Start Time','Gbusiness End Time','Gbusiness Offer Code','Gbusiness Offer Link','Gbusiness Terms & Conditions','TikTok Privacy','TikTok Comments','TikTok Duet','TikTok Stitch','Tiktok Your Brand','Tiktok Branded Content','SnapChat Title','Save To Profile','Media Url 1','Media Url 2','Media Url 3','Media Url 4','Media Url 5','Media Url 6','Media Url 7','Media Url 8','Media Url 9','Media Url 10']
items = [
('98ddd093975ff000ea492401f7a327330bf616185c9abd05dd','Your Life Is Not Over','Your story is not finished. One painful season does not mean your life is over. God can rebuild slowly, quietly, and beautifully.','#Faith #Hope #Healing #GodRestores #TheOpenDoor'),
('29c952867f3df5ea87f022cae88c062db24328483d48c82af5','Kindness Is Not Weakness','Kindness does not mean tolerating everything. You can be loving and still protect your peace. Stay kind, but walk with wisdom. Matthew 10:16.','#Kindness #Wisdom #Boundaries #Faith #ChristianEncouragement'),
('3807a76a0518b7f314e10d6407e0ea38e425e1c48ebf1bea92','Some People Are Emotionally Exhausted','Some people are not lazy. They are emotionally exhausted. Resting, crying, and asking God for strength do not make you weak. Be gentle with yourself.','#EmotionalHealing #Rest #Faith #Encouragement #TheOpenDoor'),
('fb0834b1dc80a5b7c881ee523814e176fbfe10bc7d80d0651b','Men Are Hurting Silently Too','Many men carry pressure, heartbreak, stress, and responsibility in silence. Men need encouragement, peace, and compassion too.','#MenNeedEncouragement #MentalHealth #Compassion #Faith #Healing'),
('e8f6c39df376b7030db59158cee3ff0dddf98c81fa27481eb8','Pain Changes People','Pain can change the way people trust, love, and speak. Healing takes time, and God restores broken hearts slowly and gently.','#HealingJourney #PainChangesPeople #Grace #Faith #GodRestores'),
('7f641e759c66ff4f702c7fd7edcea78da126ea11102472e1c4','Life in America Is Not Always What People Think','Many immigrants smile online while carrying loneliness, long hours, and silent pressure. If you are far from home and trying your best, God sees your sacrifice.','#ImmigrantLife #SilentStruggles #Faith #Encouragement #GodSeesYou'),
('241054bbcba047e5fa28e0453e74df02e78a7299915db47572','God Does Not Abandon Broken People','God does not only love people who look strong. He also stays close to broken people. Your quiet battles are not invisible to Him.','#GodIsNear #BrokenButLoved #Faith #Healing #ChristianEncouragement'),
('554b43f34cfb728617f0347eb662653d7146543986652acde4','Strong Women Need Rest Too','Some women carry everyone else while silently breaking inside. Strong women cry too, and they deserve rest, peace, healing, and support.','#StrongWomen #Rest #Healing #Faith #Encouragement'),
('268dcdc0bcac21170162204b4051f86c61e66c74069b3a2c2a','People Heal Differently','Healing is not the same for everyone. Some people get quiet, some isolate, and some stay busy. Stop judging someone else’s healing process.','#HealingProcess #Grace #Compassion #Faith #EmotionalHealing'),
('bf765db2d420b80bfc3e0363136cd962f80bffe9e8934dd47d','Stop Explaining Your Pain to Everyone','Not everyone will understand what hurt you. Some healing happens privately. Protect your peace, protect your heart, and keep moving forward.','#ProtectYourPeace #Healing #Faith #Peace #TheOpenDoor'),
]
first = 'What is God speaking to you through this today?'
def rowset(pairs):
    r=['']*len(header)
    for k,v in pairs.items(): r[header.index(k)] = v
    return r
for i,(hashid,title,desc,tags) in enumerate(items,1):
    date=f'{i+1:02d}/06/2026 19:00:00'
    url=f'https://app.brand2social.com/api/image-server/fetch-media?path={hashid}.mp4'
    full_desc=f'{desc} {tags}'
    rows=[
      rowset({'Schedule No':str(i),'Schedule Date/Time(DD/MM/YYYY HH:mm:ss)':date,'Common Description':full_desc,'Common First Comment':first,'Is Draft':'FALSE','Need Approval':'FALSE','Connected Profile Id':'11445','Connected Profile Name':'The Open Door','Social Media':'facebook','Description':full_desc,'First Comment':first,'Post Type':'Post','Media Url 1':url}),
      rowset({'Connected Profile Id':'11597','Connected Profile Name':'Eden Banks','Social Media':'youtube','Description':full_desc,'First Comment':first,'Post Type':'Shorts','Youtube Privacy':'Public','Youtube Title':title,'Media Url 1':url}),
      rowset({'Connected Profile Id':'11596','Connected Profile Name':'edenbanks38','Social Media':'tiktok','Description':full_desc,'Post Type':'DIRECT_POST','TikTok Privacy':'PUBLIC_TO_EVERYONE','TikTok Comments':'TRUE','TikTok Duet':'TRUE','TikTok Stitch':'TRUE','Tiktok Your Brand':'TRUE','Tiktok Branded Content':'TRUE','Media Url 1':url}),
    ]
    for base in (base_onedrive, base_allowed):
        out=os.path.join(base, f'B2S_7PM_corrected_chunk_{i:02d}.csv')
        with open(out,'w',newline='',encoding='utf-8') as f:
            w=csv.writer(f); w.writerow(header); w.writerows(rows)
print(base_onedrive)
print(base_allowed)
