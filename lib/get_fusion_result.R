library(stringr)
Args<-commandArgs(T)

setwd(Args[1])
All<-read.table(Args[2])
on<-read.table(Args[3], head = T)
FA <- read.table(Args[4])

#################################
getfa <- function(x){
    Fas <- NULL
    for(i in 1:length(x[,1])){
        FA_file <- read.table(as.character(x[,1][i]),sep ="\t")
        fa_inf <- strsplit(as.character(FA_file[1,])," ")
        Gene <- strsplit(fa_inf[[1]][1],">")[[1]][2]
        TF <- grepl("chr[0-9]+-",fa_inf[[1]][4])
        if(TF == "TRUE"){
            Chr <- strsplit(fa_inf[[1]][4],"-")[[1]][1]
            Strand <- "-"
        }else{
            Chr <- strsplit(fa_inf[[1]][4],"[+]")[[1]][1]
            Strand <- "+"
        }
        Start <- strsplit(fa_inf[[1]][5],"-")[[1]][1]
        End <- strsplit(fa_inf[[1]][5],"-")[[1]][2]
        Fa <- data.frame(Gene, Chr, Strand, Start, End)
        Fas <- rbind(Fas, Fa)
    } 
    return(Fas)
}
##################################
Gene <- c("ALK", "EML4", "KIF5B", "KLC1", "PTPN3", "STRN", "TFG")
Chr <- c("chr2", "chr2", "chr10", "chr14", "chr9", "chr2", "chr3")
Strand <- c("-", "+", "-", "+", "-", "-", "+")
Start <- c(29415640, 42396490, 32297938, 104028233, 112137746, 37070783, 100428205)
End <- c(30144432, 42559688, 32345359, 104167888, 112260590, 37193615, 100467810)
Fa_inf <- data.frame(Gene, Chr, Strand, Start, End)

TF <- Args[5]
if(length(Args) == 5){
    if(TF == "TRUE"){
        Fa_inf <- getfa(FA)
    }
}
#Fa_inf <- getfa(FA)

Fusion_AF<-c()
Fusion_Ref<-c()
sample<-c()
Fusion_Type<-c()
position_Fusion<-c()
for (i in 1:length(All[,3])){
    B<-as.numeric(All[i,3])

    position_A <- c()
    name_Gene <- c()
    for(j in 1:length(on[,1])){
        name_A <- paste(on[j,4],on[j,5],sep="_")
        if(name_A == as.character(All[i,2])){
            A = on[j,6]
            name = on[j,1]
            position_A <- c(position_A,on[j,3])
            name_Gene <- c(name_Gene,as.character(on[j,4]))
      }
    }
    x1=B/(A+B)
    x1=x1*100
    Fusion_AF<-c(Fusion_AF,x1)
    Fusion_Ref<-c(Fusion_Ref,(A+B))   

    Fusion_AF<- round(Fusion_AF,4)

    sample<-c(sample,name)
    posi<-as.character(All[i,2])
    pos<-strsplit(posi,"_",fixed=FALSE)
    position<-unlist(pos)[2]
    position<-as.numeric(position)
    position_T<-paste("ALK","-",unlist(pos)[1],sep="")
    Fusion_Type<-c(Fusion_Type, position_T)    
    for(j in 1:length(name_Gene)){
        for(k in 1:length(Fa_inf[,1])){
            if(Fa_inf[k,1] == name_Gene[j]){
                if(as.character(Fa_inf[k,3] == "+")){
                    position = as.numeric(as.character(Fa_inf[k,5])) - position + 1
                    position_A[j] = 29415640 + position_A[j] - 1
                    position_A[j]<-paste("chr2:", position_A[j], "-", as.character(Fa_inf[k,2]), ":", position,sep="")
                    position_Fusion<-c(position_Fusion,position_A[j])
                    
                }else{
                    position = as.numeric(as.character(Fa_inf[k,4])) + position -1
                    position_A[j] = 29415640 + position_A[j] - 1
                    position_A[j]<-paste("chr2:", position_A[j], "-", as.character(Fa_inf[k,2]), ":", position,sep="")
                    position_Fusion<-c(position_Fusion,position_A[j])

                }
            }
        }
    }
}
Fusion_Mut=All[,3]
#print(position_Fusion)

All_fusion<-data.frame(sample,Fusion_Type, position_Fusion,Fusion_Ref,Fusion_Mut,Fusion_AF)

write.table(All_fusion,"All-ALK-Fusion.txt",sep="\t",col.names=T,row.names=F,quote=F)
