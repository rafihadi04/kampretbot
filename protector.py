# -*- coding: utf-8 -*-
from LineAlpha import LineClient
from LineAlpha.LineApi import LineTracer
from LineAlpha.LineThrift.ttypes import Message
from LineAlpha.LineThrift.TalkService import Client
import time, datetime, random ,sys, re, string, os, json
kickMids = []

reload(sys)
sys.setdefaultencoding('utf-8')

client = LineClient()
client._tokenLogin("EtVSXqHFnTFvzbD23lua.RZ7MpjtRpd9sdYZiY3mikG.GD5GBYDF4DSpmug7JOg5OKiZlea0FlEf4t3bmlB73Z8=")

profile, setting, tracer = client.getProfile(), client.getSettings(), LineTracer(client)
offbot, messageReq, wordsArray, waitingAnswer = [], {}, {}, {}

print client._loginresult()

wait = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
   }

setTime = {}
setTime = wait["setTime"]
admin= "uaf3ee63c94eb3c3f520f2cc8cb73082a"

def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text

    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1
    client._client.sendMessage(messageReq[to], mes)

def NOTIFIED_ADD_CONTACT(op):
    try:
        sendMessage(op.param1, client.getContact(op.param1).displayName + " Thanks udah add, bot ini dibuat oleh :")
        sendMessage(op.param1, text=None, contentMetadata={'mid': admin}, contentType=13)
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ADD_CONTACT\n\n")
        return

tracer.addOpInterrupt(5,NOTIFIED_ADD_CONTACT)

'''def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    #print op
    prtngroup="[Peraturan]\n\nCek note"
    group=client.getGroup(op.param1)
    try:
        sendMessage(op.param1, client.getContact(op.param2).displayName + " WELCOME to " + group.name+"\n\n"+prtngroup)
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ACCEPT_GROUP_INVITATION\n\n")
        return

tracer.addOpInterrupt(17,NOTIFIED_ACCEPT_GROUP_INVITATION)'''

def NOTIFIED_KICKOUT_FROM_GROUP(op):
    try:
        sendMessage(op.param1, "Kicked Mid\n"+client.getContact(op.param3).mid)
        group=client.getGroup(op.param1).id
        client.kickoutFromGroup(group, op.param2)
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_KICKOUT_FROM_GROUP\n\n")
        return
tracer.addOpInterrupt(19,NOTIFIED_KICKOUT_FROM_GROUP)

def NOTIFIED_LEAVE_GROUP(op):
    try:
        sendMessage(op.param1, client.getContact(op.param2).displayName + " Good Bye\n(*´･ω･*)")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_LEAVE_GROUP\n\n")
        return

tracer.addOpInterrupt(15,NOTIFIED_LEAVE_GROUP)

def NOTIFIED_READ_MESSAGE(op):
    #print op
    try:
        if op.param1 in wait['readPoint']:
            Name = client.getContact(op.param2).displayName
            if Name in wait['readMember'][op.param1]:
                pass
            else:
                wait['readMember'][op.param1] += "\n・" + Name
                wait['ROM'][op.param1][op.param2] = "・" + Name
        else:
            pass
    except:
        pass

tracer.addOpInterrupt(55, NOTIFIED_READ_MESSAGE)

def RECEIVE_MESSAGE(op):
    msg = op.message
    bann=[]
    try:
        if msg.contentType == 0:
            try:
                if msg.to in wait['readPoint']:
                    if msg.from_ in wait["ROM"][msg.to]:
                        del wait["ROM"][msg.to][msg.from_]
                else:
                    pass
            except:
                pass
            if msg.toType==2:
                mid=client.getContact(msg.from_).mid
                name=client.getContact(msg.from_).displayName
                if "anjing"or"jing"or"njir"or"fak"or"fuck"or"kima"or"suw"or"asu"or"su"or"Anj"or"Ajg"or"Telo"or"peler"or"telo"or"Anjing"or"Kima"or"Fak" in msg.text:
                    group=client.getGroup(msg.to)
                    if msg.from_ in [bann]:
                        sendMessage(msg.to, "Kan udah ku bilang -__-")
                        client.kickoutFromGroup(msg.to, str(bann))
                        del bann[:]
                    else:
                        sendMessage(msg.to, text="Sekali lagi, ku kick @"+name, contentMetadata={'MENTION': '{"MENTIONEES":[{"M":%s,"S":"22","E":"%s"}],"EMTVER":"4"}' %(str(msg.from_),len(name)), 'EMTVER' : '4' }, contentType=0)
                        bann.append(msg.from_)
                        del bann[:]
                if msg.text == "speed":
                    start=time.time()
                    sendMessage(msg.to, "Wait...")
                    end= time.time() - start
                    sendMessage(msg.to, "%d sec" %(end))
                if msg.text in ["Lol","lol","Wkwk","wkwk","hahaha","Hahaha"]:
                    sendMessage(msg.to, "Wakakakakakak")
                if mid in admin:
                    if msg.text == "ginfo":
                        group = client.getGroup(msg.to)
                        md = "[Nama Grup]\n" + group.name + "\n\n[gid]\n" + group.id + "\n\n[Foto]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus + "\n\n[Creator]\n" + str(group.creator.displayName)
                        if group.preventJoinByTicket is False: md += "\n\nInvite lewat URL: BUKA\n"
                        else: md += "\n\nInvite lewat URL: TUTUP\n"
                        if group.invitee is None: md += "\nANGGOTA: " + str(len(group.members)) + "\n\nTertunda: 0 Orang"
                        else: md += "\nAnggota: " + str(len(group.members)) + "\n\nTertunda: " + str(len(group.invitee)) + " Orang"
                        sendMessage(msg.to,md)
                else:
                    pass
        else:
            pass
    except KeyboardInterrupt:
	       sys.exit(0)
    except Exception as error:
        print error
        print ("\n\nRECEIVE_MESSAGE\n\n")
        return

tracer.addOpInterrupt(26, RECEIVE_MESSAGE)

def SEND_MESSAGE(op):
    msg=op.message
    try:
        if msg.contentType == 13:
            sendMessage(msg.to,text=msg.contentMetadata['mid'])
        if msg.text in ['speed','sp','Speed'] :
            start=time.time()
            sendMessage(msg.to, "Wait...")
            end= time.time() -start
            sendMessage(msg.to, "%s sec" %(end))
        if msg.toType == 2:
            if msg.text == "ginfo":
                group = client.getGroup(msg.to)
                md = "[Nama Grup]\n" + group.name + "\n\n[gid]\n" + group.id + "\n\n[Foto]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus + "\n\n[Creator]\n" + str(group.creator.displayName)
                if group.preventJoinByTicket is False: md += "\n\nInvite lewat URL: BUKA\n"
                else: md += "\n\nInvite lewat URL: TUTUP\n"
                if group.invitee is None: md += "\nANGGOTA: " + str(len(group.members)) + "\n\nTertunda: 0 Orang"
                else: md += "\nAnggota: " + str(len(group.members)) + "\n\nTertunda: " + str(len(group.invitee)) + " Orang"
                sendMessage(msg.to,md)
        if msg.text in ["tagall","Tagall","Tag all"]:
            group = client.getGroup(msg.to) 
            nama = [contact.mid for contact in group.members] 
            cb = "" 
            cb2 = "" 
            strt = int(0)
            akh = int(0) 
            for md in nama: 
                akh = akh + int(6) 
                cb += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(md)+"""},"""
                strt = strt + int(7) 
                akh = akh + 1 
                cb2 += "@nrik \n" 
            cb = (cb[:int(len(cb)-1)]) 
            msg.contentType = 0 
            msg.text = cb2 
            msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}
            print(msg)
            client.sendMessage(msg)
        if 'Broadcast: 'in msg.text:
            print("\nOKE\n")
            key=msg.text[10:]
            group=client.getGroup(msg.to)
            mids= [contact.mid for contact in group.members]
            for i in range(len(mids)):
                if mids[i] in admin:
                    pass
                else:
                    sendMessage(mids[i],text=key)
            print("\nDONE_BROADCAST\n")
        else:
            pass
    except Exception as e:
        print e
        print('SEND_ERROR\n')
        return
    '''msg = op.message
    try:
        #print("\n" + str(msg.contentType))
        #print("\n" + str(msg.contentMetadata) + "\n" + str(msg.text))
        ##print("\n"+client.getContact(msg.to).displayName)
        if msg.text == "invitekick":
            group = client.getGroup(msg.to)
            gids = group.members
            Mids = [contact.mid for contact in group.members]
            i = 0
            for i in range(len(Mids)):
                client.inviteIntoGroup(msg.to, [Mids[i]] )
            del kickMids[:]
        if (msg.toType == 0) or (msg.toType == 2) or (msg.toType == 1) :
            if msg.contentType == 0:
                if msg.text == "mid":
                    sendMessage(msg.to, msg.to)
                #if msg.text == "me":
                #    sendMessage(msg.to, text=None, contentMetadata={'mid': msg.from_}, contentType=13)
                if msg.text == "gift":
                    sendMessage(msg.to, text="HADIAH BUAT KAMU", contentMetadata=None, contentType=9)
                else:
                    pass
            else:
                pass
        if (msg.toType == 2) or (msg.toType == 0) or (msg.toType == 1) :
            if msg.text == "invitekick":
                group = client.getGroup(msg.to)
                gids = group.members
                Mids = [contact.mid for contact in group.members]
                i = 0
                for i in range(len(Mids)):
                    client.inviteIntoGroup(msg.to, [Mids[i]] )
                del kickMids[:]
            if msg.contentType == 0:
                if msg.text == "invitekick":
                    group = client.getGroup(msg.to)
                    gids = group.members
                    Mids = [contact.mid for contact in group.members]
                    i = 0
                    for i in range(len(Mids)):
                        client.inviteIntoGroup(msg.to, [Mids[i]] )
                    del kickMids[:]
                if msg.text == "me":
                    sendMessage(msg.to, text=None, contentMetadata={'mid': msg.from_}, contentType=13)
                if msg.text == "mid":
                    sendMessage(msg.to, msg.from_)
                if msg.text == "gid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "ginfo":
                    group = client.getGroup(msg.to)
                    md = "[Nama Grup]\n" + group.name + "\n\n[gid]\n" + group.id + "\n\n[Foto]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                    if group.preventJoinByTicket is False: md += "\n\nInvite lewat URL: BUKA\n"
                    else: md += "\n\nInvite lewat URL: TUTUP\n"
                    if group.invitee is None: md += "\nANGGOTA: " + str(len(group.members)) + "\n\nTertunda: 0 Orang"
                    else: md += "\nAnggota: " + str(len(group.members)) + "\n\nTertunda: " + str(len(group.invitee)) + " Orang"
                    sendMessage(msg.to,md)
                if "gname:" in msg.text:
                    key = msg.text[6:]
                    group = client.getGroup(msg.to)
                    group.name = key
                    client.updateGroup(group)
                    sendMessage(msg.to,"Nama Grup di ubah menjadi "+key)
                if msg.text == "url":
                    sendMessage(msg.to,"line://ti/g/" + client._client.reissueGroupTicket(msg.to))
                if msg.text == "qropen":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == False:
                        sendMessage(msg.to, "sudah terbuka")
                    else:
                        group.preventJoinByTicket = False
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL Terbuka")
                if msg.text == "qrclose":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == True:
                        sendMessage(msg.to, "sudah tertutup")
                    else:
                        group.preventJoinByTicket = True
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL \nTertutup")
                if "kicktoo:" in msg.text:
                    key = msg.text[8:]
                    client.kickoutFromGroup(msg.to, [key])
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+" Bye")
                if "kick:" in msg.text:
                    key = msg.text[5:]
                    group = client.getGroup(msg.to)
                    Names = [contact.displayName for contact in group.members]
                    Mids = [contact.mid for contact in group.members]
                    if key in Names:
                        kazu = Names.index(key)
                        sendMessage(msg.to, "Daaah " +Mids[kazu])
                        client.kickoutFromGroup(msg.to, [""+Mids[kazu]+""])
                        contact = client.getContact(Mids[kazu])
                        sendMessage(msg.to, ""+contact.displayName+"")
                    else:
                        sendMessage(msg.to, "Nda Ketemu")
                if msg.text == "cancel":
                    group = client.getGroup(msg.to)
                    if group.invitee is None:
                        sendMessage(op.message.to, "Tidak ada data")
                    else:
                        gInviMids = [contact.mid for contact in group.invitee]
                        client.cancelGroupInvitation(msg.to, gInviMids)
                        sendMessage(msg.to, str(len(group.invitee)) + " Selesai")
                if "invite:" in msg.text:
                    key = msg.text[8:]
                    client.findAndAddContactsByMid(key)
                    client.inviteIntoGroup(msg.to, [key])
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+" I invited you")
                if "show:" in msg.text:
                    key = msg.text[5:]
                    group = client.getGroup(msg.to)
                    Names = [contact.displayName for contact in group.members]
                    Mids = [contact.mid for contact in group.members]
                    if key in Names:
                        nama = Names.index(key)
                        sendMessage(msg.to, ""+Mids[nama]+"")
                        sendMessage(msg.to, text=None, contentMetadata={'mid': Mids[nama]}, contentType=13)
                if msg.text == "time":
                    sendMessage(msg.to, "Waktu :" + datetime.datetime.today().strftime('%Y/%m/%d %H:%M:%S'))
                if msg.text == "gift":
                    sendMessage(msg.to, text="HADIAH BUAT KAMU", contentMetadata={'PRDID': '40ed630f-22d2-4ddd-8999-d64cef5e6c7d','PRDTYPE': 'THEME','MSGTPL': '5'}, contentType=9)
                if msg.text == "set":
                    sendMessage(msg.to, "SET POINT TELAH DIBUAT")
                    try:
                        del wait['readPoint'][msg.to]
                        del wait['readMember'][msg.to]
                    except:
                        pass
                    wait['readPoint'][msg.to] = msg.id
                    wait['readMember'][msg.to] = ""
                    wait['setTime'][msg.to] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    wait['ROM'][msg.to] = {}
                    print wait
                if msg.text == "tes":
                    if msg.to in wait['readPoint']:
                        if wait["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait["ROM"][msg.to].items():
                                print rom
                                chiya += rom[1] + "\n"

                        sendMessage(msg.to, "TERCYDUK KAMU!!! \n%s\n\n YG NGABAIKAN:\n%s\n\n HAYOLO\nby RambolBot"  %(wait['readMember'][msg.to],chiya) )
                    else:
					    sendMessage(msg.to, "SET POINT BELUM TERBUAT")
                if msg.text == "stop":
                    sendMessage(msg.to, "SET POINT TELAH DIBUANG")
                    try:
                        del wait['readPoint'][msg.to]
                        del wait['readMember'][msg.to]
                    except:
                        print error
                        print ("\n\nSETPOINTDELETE\n\n")
                if "cinfo:" in msg.text:
                    key = msg.text[6:]
                    group = client.getGroup(msg.to)
                    Names = [contact.displayName for contact in group.members]
                    Mids = [contact.mid for contact in group.members]
                    nama = Names.index(key)
                    contactss = Mids[nama]
                    kontak = client.getContact(contactss)
                    md = "[Nama]\n" + kontak.displayName + "\n\n[mid]\n" +contactss+ "\n\n[foto]\nhttp://obs.line-apps.com" +kontak.picturePath+ "\n\n[bio]\n" +kontak.statusMessage+ "\nby RambolBot"
                    sendMessage(msg.to,md)
                    #client.sendImageWithURL(msg.to, 'http://obs-sg.line-apps.com'+kontak.picturePath+"/")
                if msg.text == "list" :
                    group = client.getGroup(msg.to)
                    gids = group.members
                    Mids = [contact.mid for contact in group.members]
                    Nama = [contact.displayName for contact in group.members]
                    md = "[List Member]\n"
                    i = 0
                    for i in range(len(Mids)):
                       md += "\n- " + Nama[i]
                    sendMessage(msg.to, md)
                if msg.text == "stiker" :
                    sendMessage(msg.to, text=None, contentMetadata={'packageId': '1','stickerId': '1'}, contentType=7)
                if msg.text == "kickall" :
                    group = client.getGroup(msg.to)
                    gids = group.members
                    Mids = [contact.mid for contact in group.members]
                    i = 0
                    kickMids.extend(Mids)
                    for i in range(len(Mids)):
                       client.kickoutFromGroup(msg.to, [Mids[i]] )
                if msg.text == "mention" :
                    group = client.getGroup(msg.to)
                    Mids = [contact.mid for contact in group.members]
                    nama = [contact.displayName for contact in group.members]
                    i = 0
                    md = "[Anggota]\n"
                    konten = []
                    haloold=[0]
                    start =10
                    for i in range(len(Mids)):
                        kazu = Mids.index(Mids[i])
                        start = start  + haloold[i]
                        end = start + len(nama[kazu])
                        konten.append({"M" : "%s","S" : "%s","E":"%s"} %(str(Mids[i]),start,end))
                        start += 2
                        md += "\n@" + str(nama[kazu])
                        haloold.append(len(nama[kazu]))
                    print(konten)
                    sendMessage(msg.to, text=md, contentMetadata={'MENTION': '{"MENTIONEES": %s }' %s(konten)} , contentType=0)
            if msg.contentType == 13:
                key = msg.contentMetadata['mid']
                sendMessage(msg.to, "Mid :\n" + str(key))
        else:
            pass

    except Exception as e:
        print e
        print ("\n\nSEND_MESSAGE\n\n")
        return'''

tracer.addOpInterrupt(25,SEND_MESSAGE)

while True:
    tracer.execute()
