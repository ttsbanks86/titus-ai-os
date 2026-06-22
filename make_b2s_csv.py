import csv
out = r'C:\Users\tbank\OneDrive\NOLO Video Scheduling\Current Project\Brand2Social_7PM_Main_FB_TikTok_2026-06-02.csv'
header = ['Schedule No','Schedule Date/Time(DD/MM/YYYY HH:mm:ss)','Common Description','Common First Comment','Is Draft','Need Approval','Errors','Connected Profile Id','Connected Profile Name','Social Media','Description','First Comment','Post Type','Youtube Privacy','Youtube Title','Youtube Thumbnail','Pinterest Title','Pinterest Boards','Pinterest Board Sections','Pinterest Link','Pinterest Cover Image','Gbusiness Button Type','Gbusiness Url','Gbusiness Title','Gbusiness Start Date','Gbusiness End Date','Gbusiness Start Time','Gbusiness End Time','Gbusiness Offer Code','Gbusiness Offer Link','Gbusiness Terms & Conditions','TikTok Privacy','TikTok Comments','TikTok Duet','TikTok Stitch','Tiktok Your Brand','Tiktok Branded Content','SnapChat Title','Save To Profile','Media Url 1','Media Url 2','Media Url 3','Media Url 4','Media Url 5','Media Url 6','Media Url 7','Media Url 8','Media Url 9','Media Url 10']
urls = ['98ddd093975ff000ea492401f7a327330bf616185c9abd05dd','29c952867f3df5ea87f022cae88c062db24328483d48c82af5','3807a76a0518b7f314e10d6407e0ea38e425e1c48ebf1bea92','fb0834b1dc80a5b7c881ee523814e176fbfe10bc7d80d0651b','e8f6c39df376b7030db59158cee3ff0dddf98c81fa27481eb8','7f641e759c66ff4f702c7fd7edcea78da126ea11102472e1c4','241054bbcba047e5fa28e0453e74df02e78a7299915db47572','554b43f34cfb728617f0347eb662653d7146543986652acde4','268dcdc0bcac21170162204b4051f86c61e66c74069b3a2c2a','bf765db2d420b80bfc3e0363136cd962f80bffe9e8934dd47d']
dates = [f'{d:02d}/06/2026 19:00:00' for d in range(2,12)]
desc = 'A timely word of encouragement from The Open Door with Eden. Pause, reflect, and let this message strengthen your faith today. #Faith #Encouragement #TheOpenDoor'
first = 'What is God speaking to you through this today'
rows=[]
def rowset(pairs):
    r=['']*len(header)
    for k,v in pairs.items(): r[header.index(k)] = v
    return r
for i,(date,u) in enumerate(zip(dates,urls),1):
    url=f'https://app.brand2social.com/api/image-server/fetch-media?path={u}.mp4'
    rows.append(rowset({'Schedule No':str(i),'Schedule Date/Time(DD/MM/YYYY HH:mm:ss)':date,'Common Description':desc,'Common First Comment':first,'Is Draft':'FALSE','Need Approval':'FALSE','Connected Profile Id':'11445','Connected Profile Name':'The Open Door','Social Media':'facebook','Description':desc,'First Comment':first,'Post Type':'Post','Media Url 1':url}))
    rows.append(rowset({'Connected Profile Id':'11596','Connected Profile Name':'edenbanks38','Social Media':'tiktok','Description':desc,'Post Type':'DIRECT_POST','TikTok Privacy':'PUBLIC_TO_EVERYONE','TikTok Comments':'TRUE','TikTok Duet':'TRUE','TikTok Stitch':'TRUE','Tiktok Your Brand':'TRUE','Tiktok Branded Content':'TRUE','Media Url 1':url}))
with open(out,'w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(header); w.writerows(rows)
print(out)
