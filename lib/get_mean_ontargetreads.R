Args <- commandArgs()

setwd(Args[6])
#table=read.table(paste(Args[7],".txt",sep=""),header=F,sep="\t",stringsAsFactors=FALSE)
table=read.csv(paste(Args[7],".txt",sep=""),header=T,sep="\t",stringsAsFactors=FALSE,check.names=F)
row.names(table) <- table[,1]
name <- colnames(table)
index <- grep("_ontarget$",name,perl=TRUE,value=FALSE)

fcal <- table[,c(index)]
dataM <-c()
if(length(index) == 1){
    for (j in 1:length(table[,1])){
        dataM[j] <- fcal[j]
    }
}else{
    for (j in 1:length(fcal[,1])){
        dataM[j] <- apply(fcal[j,],1,mean)
    }
}
table$mean_ontar_reads <- dataM
write.table(table,paste(Args[7],"_Final.xls",sep=""),sep="\t",quote = FALSE,row.names = FALSE,col.names = TRUE)
