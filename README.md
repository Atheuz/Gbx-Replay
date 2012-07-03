Gbx Replay
==========

Tool for receiving information about a TrackMania Nations Forever replay or challenge.

How-To
------

To use on a single file, run the following command:

    python main.py -f filename.gbx

This will work on a Gbx replay file or a Gbx challenge file.

To use on a directory, run the following command:

    python main.py -p PATH


Examples of output
------------------

### For single files:

#### Gbx replay:

    ('xml', '<header type="replay" version="TMr.7" exever="2.11.16"><challenge uid="jGE4w5ArkNSob027quREeX9RYm3"/><times best="55890" respawns="0" stuntscore="38" validable="1"/></header>')
    ('replay_timestamp', '0:00:55.890000')
    ('uid', 'jGE4w5ArkNSob027quREeX9RYm3')
    ('author_name', 'entropist')
    ('filename', 'example_replay (1).Gbx')
    ('environment', 'Stadium')
    ('gbx_type', 'replay')
    ('replay_type', 7)
    ('replay_time', 55890)
    ('replay_version', 2)
    ('nickname', 'Ghetto Wizard')
    ('login', 'atheuz')

#### Gbx challenge:
    
    ('xml', '<header type="challenge" version="TMc.6" exever="2.11.26"><ident uid="WdqRMG5RDYTlleZx2LnD13nQ7Wi" name="SA5 - Eurotrash" author="entropist"/><desc envir="Stadium" mood="Day" type="Race" nblaps="0" price="1375" /><times bronze="62000" silver="50000" gold="45000" authortime="41200" authorscore="41200"/><deps><dep file="Skins\\Any\\Advertisement\\SignRight.bik"/><dep file="Skins\\Any\\Advertisement\\Advert3.zip"/><dep file="Skins\\Any\\Advertisement\\Advert2.zip"/><depfile="Skins\\Any\\Advertisement\\SignLeft.bik"/><dep file="Skins\\Any\\Advertisement\\Advert1.zip"/><dep file="Skins\\Any\\Advertisement\\SignUp.bik"/></deps></header>')
    ('uid', 'WdqRMG5RDYTlleZx2LnD13nQ7Wi')
    ('gold', 45000)
    ('author', 41200)
    ('copper_price', 1375)
    ('track_type', 0)
    ('mood_name', 'Day')
    ('filename', 'example_challenge (3).Gbx')
    ('author_name', 'entropist')
    ('environment', 'Stadium')
    ('track_name', 'SA5 - Eurotrash')
    ('author_score', 41200)
    ('gbx_type', 'challenge')
    ('challenge_version', 6)
    ('multi_lap', 0)
    ('silver', 50000)
    ('bronze', 62000)
    
And it will create a thumbnail in the 'output' directory.


### For directories:
    
#### For a directory of Gbx replays:

In this scenario it will create an csvfile with the trackname as the filename. In the csvfile it will in descending order list the replay author along with the replay time and nothing more:

    Ghetto Wizard,32610
    Ghetto Wizard,32690
    Ghetto Wizard,32710
    Ghetto Wizard,32760
    Ghetto Wizard,32840
    Ghetto Wizard,32870
    Ghetto Wizard,33120
    Ghetto Wizard,33320
    Ghetto Wizard,33470
    Ghetto Wizard,33590
    Ghetto Wizard,34240
    Ghetto Wizard,34660
    Ghetto Wizard,34730
    Ghetto Wizard,35040

#### For a directory of Gbx challenges:

In this scenario it will create thumbnails for the challenges and nothing more.
