

from _lspro import *
def search_lspro_source(source=None,searchterm="") :
    if searchterm == "" :
        keyboard = xbmc.Keyboard('','Search[Use one syllable only;no space]')
        keyboard.doModal()
        if not (keyboard.isConfirmed() == False):
                newStr = keyboard.getText()
                if len(newStr) == 0 :
                    return 
        else:
            #xbmc.log("No Search term found",#xbmc.logNOTICE)
            return
        searchterm = newStr.lower().replace(' ', '')
        changesetting = False
        if groupm3ulinks == 'true':
            addon.setSetting('groupm3ulinks', 'false')
            changesetting = True
        if addon.getSetting('donotshowbychannels') == 'false':
            addon.setSetting('donotshowbychannels', 'true')
            changesetting = True
    import workers
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Creating Search')
        
    m3upat = re.compile(r"\s?#EXTINF:.+?,.*?%s.*?[\n\r]+[^\r\n]+" %searchterm,  re.IGNORECASE )
        
    link = ''
    ALLexlink =allitems= []
    threads = []
    if not source:
        s_f = os.path.join(profile,'source_file')
        sources = json.loads(open(s_f,"r").read())
    else:
        sources = [source]
    def processthreads(threads):
        [i.start() for i in threads]
        timeout =10
        for i in range(0, timeout * 2):
            progress.update(30+i,"Please Wait %s Seconds" %str(i))
            is_alive = [x.is_alive() for x in threads]
            if all(x == False for x in is_alive): break
            time.sleep(0.5)
            #[i.join() for i in threads]
        try: progress.close()
        except: pass        
    def getSearchData(url):
            
            k=None
            soup = getData(url,searchterm=searchterm)
            #progress.update(40, "Searching URL")
            if soup:
                allitem = soup("item")
                [getItems(allitem[index], FANART) for index,i in enumerate(allitem) if i.get('title') and searchterm in i.get('title').lower().strip()]
                exlink = soup("externallink")
                if len(exlink) > 0:
                    allexlinks= [i.string for index,i in  enumerate(exlink) if not i.string is None  ]
                    k=find_ex_links(allexlinks)
                if k:
                    k=find_ex_links(allexlinks)
                if k:
                    k=find_ex_links(allexlinks)
                if k:
                    k=find_ex_links(allexlinks)          
    def find_ex_links(sources): 
        for link in sources:
            progress.update(20, "Finding External sources")
            soup = getSoup(url=link)
            if soup:
                if not isinstance(soup,BeautifulSOAP):
                
                        matchs = m3upat.findall(soup)
                        for match in matchs : threads.append(workers.Thread(parse_m3u, match))
                        continue
                allitem = soup("item")
                progress.update(25,"Items found %s" %len(allitem))
                [getItems(allitem[index], FANART) for index,i in enumerate(allitem) if i.get('title') and searchterm in i.get('title').lower().strip()]
                exlink =soup('externallink')
                x= ['py'+cacheKey(i.string) for index,i in  enumerate(exlink) if not i.string is None  ]
                #xbmc.log(str(x),#xbmc.logNOTICE) 
                progress.update(35,"processing externallink : %s" %len(exlink))
                if len(exlink)>0:
                    return [i.string for index,i in  enumerate(exlink) if not i.string is None  ]

    getexitems = find_ex_links(sources)
    
    ##xbmc.log(str("processing externallink : %s" %len(getexitems)),#xbmc.logNOTICE) 
    if getexitems:
    
            #ll= [i.string for index,i in  enumerate(getexitems) if not i.string is None  ]
    
            for link in getexitems :
                #xbmc.log(str('py'+cacheKey(link)),#xbmc.logNOTICE) 
                threads.append(workers.Thread(getSearchData, link)) 
            progress.update(40,"processing Threads : %s" %len(threads))
    try: progress.close()
    except: pass
    #Not sure why these change dont take place
    if changesetting:
        addon.setSetting('groupm3ulinks', 'true')
        addon.setSetting('donotshowbychannels', 'false')    
    if threads:
        processthreads(threads)

    ##xbmc.log("[addon.live.streamsproSearchURL-%s]:Items found %s" %(str(url), str(len(allitems))),#xbmc.logNOTICE)         
    #items = [getItems(allitem[index], fanart) for index,i in enumerate(allitems[0])]
    
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
