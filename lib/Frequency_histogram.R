Args <- commandArgs()

setwd(Args[6])
library(Cairo)
#list.files()
a=read.table(paste(Args[7],".xls",sep=""),header=F,sep="\t",stringsAsFactors=FALSE)
b<-a[which(a[,2]<100),2]
CairoPDF(paste(Args[7],".pdf",sep=""))
hist(b,col='blue',border='yellow',main='UMI',xlab='UMI Reads',breaks=100)
dev.off()
