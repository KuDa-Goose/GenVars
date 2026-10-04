Args <- commandArgs()

setwd(Args[6])
Sample_Dirs <- Sys.glob("Sample*") 

d<-data.frame()

d=read.table("snp_indel.xls",header=T,sep="\t",stringsAsFactors=FALSE)
b=read.table("deep.xls",header=T,sep="\t",stringsAsFactors=FALSE)
n=nrow(d)
for(j in 1:n){
  if(d[j,2]==0){
    d[j,2]<-b[j,2]
    d[j,3]<-0
    d[j,4]<-0
  }  else{
      d[j,2]=d[j,2]
     }
}
for(j in 1:n){
  if(d[j,5]==0){
    d[j,5]<-b[j,3]
    d[j,6]<-0
    d[j,7]<-0
  }  else{
      d[j,5]=d[j,5]
     }
}
for(j in 1:n){
  if(d[j,8]==0){
    d[j,8]<-b[j,4]
    d[j,9]<-0
    d[j,10]<-0
  }  else{
      d[j,8]=d[j,8]
     }
}
for(j in 1:n){
  if(d[j,11]==0){
    d[j,11]<-b[j,5]
    d[j,12]<-0
    d[j,13]<-0
  }  else{
      d[j,11]=d[j,11]
     }
}
for(j in 1:n){
  if(d[j,14]==0){
    d[j,14]<-b[j,6]
    d[j,15]<-0
    d[j,16]<-0
  }  else{
      d[j,14]=d[j,14]
     }
}
for(j in 1:n){
  if(d[j,17]==0){
    d[j,17]<-b[j,7]
    d[j,18]<-0
    d[j,19]<-0
  }  else{
      d[j,17]=d[j,17]
     }
}
for(j in 1:n){
  if(d[j,20]==0){
    d[j,20]<-b[j,8]
    d[j,21]<-0
    d[j,22]<-0
  }  else{
      d[j,20]=d[j,20]
     }
}
for(j in 1:n){
  if(d[j,23]==0){
    d[j,23]<-b[j,9]
    d[j,24]<-0
    d[j,25]<-0
  }  else{
      d[j,23]=d[j,23]
     }
}
for(j in 1:n){
  if(d[j,26]==0){
    d[j,26]<-b[j,10]
    d[j,27]<-0
    d[j,28]<-0
  }  else{
      d[j,26]=d[j,26]
     }
}
for(j in 1:n){
  if(d[j,29]==0){
    d[j,29]<-b[j,11]
    d[j,30]<-0
    d[j,31]<-0
  }  else{
      d[j,29]=d[j,29]
     }
}
for(j in 1:n){
  if(d[j,32]==0){
    d[j,32]<-b[j,12]
    d[j,33]<-0
    d[j,34]<-0
  }  else{
      d[j,32]=d[j,32]
     }
}
for(j in 1:n){
  if(d[j,35]==0){
    d[j,35]<-b[j,13]
    d[j,36]<-0
    d[j,37]<-0
  }  else{
      d[j,35]=d[j,35]
     }
}
for(j in 1:n){
  if(d[j,38]==0){
    d[j,38]<-b[j,14]
    d[j,39]<-0
    d[j,40]<-0
  }  else{
      d[j,38]=d[j,38]
     }
}
for(j in 1:n){
  if(d[j,41]==0){
    d[j,41]<-b[j,15]
    d[j,42]<-0
    d[j,43]<-0
  }  else{
      d[j,41]=d[j,41]
     }
}
for(j in 1:n){
  if(d[j,44]==0){
    d[j,44]<-b[j,16]
    d[j,45]<-0
    d[j,46]<-0
  }  else{
      d[j,44]=d[j,44]
     }
}
for(j in 1:n){
  if(d[j,47]==0){
    d[j,47]<-b[j,17]
    d[j,48]<-0
    d[j,49]<-0
  }  else{
      d[j,47]=d[j,47]
     }
}
for(j in 1:n){
  if(d[j,50]==0){
    d[j,50]<-b[j,18]
    d[j,51]<-0
    d[j,52]<-0
  }  else{
      d[j,50]=d[j,50]
     }
}
for(j in 1:n){
  if(d[j,53]==0){
    d[j,53]<-b[j,19]
    d[j,54]<-0
    d[j,55]<-0
  }  else{
      d[j,53]=d[j,53]
     }
}
for(j in 1:n){
  if(d[j,56]==0){
    d[j,56]<-b[j,20]
    d[j,57]<-0
    d[j,58]<-0
  }  else{
      d[j,56]=d[j,56]
     }
}
for(j in 1:n){
  if(d[j,59]==0){
    d[j,59]<-b[j,21]
    d[j,60]<-0
    d[j,61]<-0
  }  else{
      d[j,59]=d[j,59]
     }
}
for(j in 1:n){
  if(d[j,63]==0){
    d[j,63]<-b[j,22]
    d[j,64]<-0
    d[j,65]<-0
  }  else{
      d[j,63]=d[j,63]
     }
}
for(j in 1:n){
  if(d[j,66]==0){
    d[j,66]<-b[j,23]
    d[j,67]<-0
    d[j,68]<-0
  }  else{
      d[j,66]=d[j,66]
     }
}


sample_name <- substring(Sample_Dirs[1], 7)
outTab_name <- paste("snp_indel_deep_", ".xls", sep=sample_name)

write.table(d, outTab_name , sep="\t",col.names=T,row.names=F,quote=F)

#write.table(d,"snp_indel_deep.xls",sep="\t",col.names=T,row.names=F,quote=F)

