import sys;
class node:
    def __init__(self,gene_id,gene_set,cluster_id):
        self.id=gene_id;
        self.gset=gene_set;
        self.cid=cluster_id;
        self.pts=0;
        self.ntype=1;
        self.clist=list();
        self.visited=0;
        self.cidlist=list();
    def pr(self):
        print 'id:',self.id
        print 'gset:',self.gset
        print 'cid:',self.cid
        print 'pts:',self.pts
        print 'type:',self.ntype
        print 'clist:',self.clist
        print 'visited:',self.visited
class __redirection__: 
    def __init__(self): 
      self.buff='' 
      self.__console__=sys.stdout 

    def write(self, output_stream): 
      self.buff+=output_stream 
  
    def to_console(self): 
      sys.stdout=self.__console__ 
      print self.buff 
  
    def to_file(self, file_path):
      f=open(file_path,'w') 
      sys.stdout=f 
      print self.buff 
      f.close() 

    def flush(self): 
      self.buff='' 
 
    def reset(self): 
      sys.stdout=self.__console__ 	
def distance(ns,i,j):
    return 1-float(len(ns[i].gset&ns[j].gset))/float(len(ns[i].gset|ns[j].gset))
	
def dbscan(res,uset,link):
    r_obj=__redirection__() 
    sys.stdout=r_obj;
    url_relates_dic={};
    for l in open(link,'r'):
        s=l.strip().split(',')
        l=int(s[0])
        r=int(s[1])
        if l not in url_relates_dic:
            url_relates_dic[l]=set();
        if r not in url_relates_dic:
            url_relates_dic[r]=set();
        url_relates_dic[l].add(r);
        url_relates_dic[r].add(l);
        
    nodes=list();
    t=1;
    f_final=open('./res/URL_Relates.csv','w');
    for l in open(uset,'r'):
        s=l.strip().strip(',').split(',')
        l=int(s[0]);
        r=set(map(int,s[1:]))
        if l not in url_relates_dic:continue;
        s1=url_relates_dic[l];
        s2=set();
        for ts1 in s1:
            s2=s2|url_relates_dic[ts1];
        if len(r&s2)==0:continue;
        nodes.append(node(l,r&s2,t));
        f_final.write(s[0]);
        for ge in r&s2:
            f_final.write(','+str(ge));
        f_final.write('\n');
        t=t+1;
    f_final.close();
    n_len=len(nodes);
    print 'nodes_count:',n_len,'\n'

    #cluster
    dis=[([0] * n_len) for i in range(n_len)]
    eps=0.726561679101;
    #eps=0.65
    minpts=4;
    for i in range(n_len):
        for j in range(i,n_len):
            dis[j][i]=distance(nodes,i,j);
            dis[i][j]=dis[j][i]
    #for i in range(n_len):
    #    dis[i].sort()
    for i in range(n_len):
        for j in range(i+1,n_len):
            if dis[i][j]<eps:
                nodes[i].pts+=1
                nodes[j].pts+=1
                
    corenodes=list();
    for n in nodes:
        if n.pts>=minpts:
            n.ntype=3;
            corenodes.append(n);
    for i in range(len(corenodes)):
        for j in range(i+1,len(corenodes)):
            if distance(corenodes,i,j)<eps:
                corenodes[i].clist.append(j)
                corenodes[j].clist.append(i)
    print 'core_count:',len(corenodes),'\n'

    for i in range(len(corenodes)):
        ps=list();
        if corenodes[i].visited:continue;
        ps.append(i);
        while len(ps)>0:
            v=ps.pop();
            corenodes[v].visited=1;
            for j in range(len(corenodes[v].clist)):
                if corenodes[corenodes[v].clist[j]].visited:continue;
                corenodes[corenodes[v].clist[j]].cid=corenodes[i].cid;
                ps.append(corenodes[v].clist[j]);
                
    dlink=set()
    for i in range(n_len):
        if nodes[i].ntype==3:continue;
        for j in range(len(corenodes)):
            if (1-float(len(nodes[i].gset&corenodes[j].gset))/float(len(nodes[i].gset|corenodes[j].gset)))<eps:
                nodes[i].ntype=2;
                nodes[i].cidlist.append(corenodes[j].cid);
                dlink.add(tuple((min(nodes[i].id,corenodes[j].id),max(nodes[i].id,corenodes[j].id))))
    clink={tuple((min(n.id,corenodes[c].id),max(n.id,corenodes[c].id))) for n in corenodes for c in n.clist}
    link=clink|dlink
    print 'links:',link,'\n'
    f=open('./res/URL_link.csv','w');
    for t in link:
        f.write(str(t[0])+','+str(t[1])+'\n')
    f.close()

    output={};
    for n in corenodes:
        if n.cid not in output:
            output[n.cid]=set();
        output[n.cid].add(n.id);    
    print 'only core point:',output,'\n'
    for n in nodes:
        if n.ntype!=2:continue;
        for clid in n.cidlist:
            output[clid].add(n.id);
    print 'all:',output,'\n'
    f=open('./res/Curl.csv','w');
    f.write('id');
    f.write('\n');
    for n in nodes:
        if n.ntype==1:continue;
        f.write(str(n.id));
        f.write('\n');
    f.close();

    f=open('./res/URL_cluster.csv','w');
    for o in output:
        for oo in output[o]:
            f.write(str(oo));
            f.write(',');
        f.write('\n');
    f.close()
    print 'finish clustering \n'
    res=r_obj.buff
    return res;

#dbscan()