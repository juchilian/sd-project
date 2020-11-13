# sd-project
**SD工学演習プロジェクト**  
(Googleスライド)<https://docs.google.com/presentation/d/1etpcOGrdUzuPp5GeeEU-b6uY9f1UJ5I0BhD9hmIuGak/edit?usp=sharing>

**sd-project[miro]**
<https://miro.com/welcomeonboard/ZJwFbvRwlqD5JeYIpDtvRglvvTXwTa3WafQ1k2p5LipMgQ0sNVbAm0vJn3Um2yor>

**sd-project[クラス、変数定義]**
<https://docs.google.com/spreadsheets/d/1rZuYTwfBg2fiRPgnmv7i9B-a1WxZP_BdaMZDMcfW_kY/edit?usp=sharing>

Gitコマンド  
git checkout [ブランチ名]  
⇒作業するブランチに移動  
オススメサイト  
<https://qiita.com/shh-nkmr/items/fde133cbdfa5f0092be1>


Git構造  
main・・・リリース用(完成品をアップする) 基本いじらない  
develop・・・基本となるゲーム開発をするブランチ(担当：藤井、ゲーム機能をゴリゴリ作りこむ)  
  feature_online・・・オンライン対戦機能開発(担当：菊池、サーバー設定etc)  
  feature_pulse・・・脈拍の機能開発(担当：福井、ラズパイで脈拍検知するコード作成)  
  feature_eye_detect・・・視線の検出機能（担当：福井）  

作業を開始する前にターミナルですること  
1.git branch (自分がどこのブランチにいるか知る)  
2.git checkout [branch名] (自分が作業するブランチに移動)   

branchがない場合は  
git branch [branch名] で新しいブランチを作れます。  

git commitしたらpushも同時にしていいよ  

 参考 Youtube-The gitflow workflow - in less than 5 mins.  
 [https://youtube.com/watch?v=1SXpE08hvGs]
