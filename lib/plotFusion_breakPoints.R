#!/usr/bin/Rscript
library(Cairo)
args <- commandArgs(TRUE)

inputData <- args[1]

barCode <- substring(inputData, 7,9)
dataI=read.table(inputData,sep="\t",head=T)

jpgName = paste("fusion_ALK_EML4_", ".jpg", sep=barCode)
CairoJPEG(jpgName,width=10000,height=5000, res =800)


high <- max(dataI$SampleX)
#par(mfrow=c(2,5))
par(mar=c(4.3, 5, 6.7, 2) + 0.2)
plot(dataI$position,dataI$SampleX,type="b",pch=17,lty=1,col="red",
    main=(paste("Fusion-ALK_EML4", barCode, sep="_") ),xlab="position",ylab="depth",cex.axis=2,cex.main=2,cex.lab=2)
#lines(dataI$position,dataI$Sample084,type="b",pch=17,lty=2,col="blue")

abline(v=175,lty=5,col="black")
#text(175,high,"42493956",pos=2,cex=c(1),col="purple",srt=90)
text(174,71,"42493956",pos=2,cex=c(1),col="black",srt=90)

abline(v=176,lty=7,col="blue")
#text(176,high,"29448092",pos=4,cex=c(1),col="blue",srt=90)
text(177,1,"29448092",pos=4,cex=c(1),col="blue",srt=90)

sampleLabel <- paste("Sample", barCode, sep="")
#legend("topright",inset=.1,title="",c("Sample083","Sample084"),lty=c(1,2),cex=c(2,2),pch=c(21,17),col=c("red","blue"))
#legend("topright",inset=.02,title="Barcode_ID",c(sampleLabel),lty=c(0.8),cex=c(1.2),pch=c(17),col=c("red"))
legend("topright",inset=.02,title=expression(bold("Barcode_ID")),title.col="purple",c(sampleLabel),lty=c(0.8),cex=c(1.2),pch=c(17),col=c("red"))
dev.off()
