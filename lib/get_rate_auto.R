Args <- commandArgs(T)
setwd(Args[1])
#Rscript R0 path get_rate.bed all_sample.bed#
library(Cairo)
a<-data.frame()
filenamea<-c()

b<-data.frame()
filename<-c()

d<-data.frame()
probe<-data.frame()

d_image<-data.frame()
probe_image<-data.frame()
f<-c()
f_p<-c()
k<-list()

a<-read.table(Args[2],sep="\t",head=F)
filenamea=a[,5]
filenamea<-as.character(filenamea)

for (j in 1:length(filenamea)){
    probe<-list()
    probe_image<-list()
    d<-data.frame()
    d_image<-data.frame()
    f_p<-c(0)
    gmax<-c(0)
    f<-c(0)
    if (a[j,6]=="+"){
        probe_lt=a[j,2]
        probe_gt=a[j,3]+300
        position<-c(probe_lt:probe_gt)

        probe_image_lt=a[j,2]-5
        probe_image_gt=a[j,3]+300
        position_image<-c(probe_image_lt:probe_image_gt)
    }else{
        probe_lt=a[j,2]-300
        probe_gt=a[j,3]
        position<-c(probe_lt:probe_gt)

        probe_image_lt=a[j,2]-300
        probe_image_gt=a[j,3]+5
        position_image<-c(probe_image_lt:probe_image_gt)
    }
    d<-data.frame(position,f)
    d_image<-data.frame(position_image,f_p)
    colnames(d_image)=c("position","f_p")

    b<-read.table(Args[3],sep="\t",head=F)
    filename=b[,1]
    filename<-as.character(filename)

    sample_sum=length(filename)

    for(i in 1:length(filename)){
         sample_name<-c(paste(filename[i],"-",sep=""))
         k[[i]]<-read.table(paste(filename[i],filenamea[j],".deep",sep=""),sep="\t",head=F)
         colnames(k[[i]])=c("chr","position",filename[i])
         k[[i]][,1]<-as.character(k[[i]][,1])
         a[j,1]<-as.character(a[j,1])

         probe[[i]]<- data.frame(k[[i]][which(k[[i]][,1]==a[j,1] & k[[i]][,2]>=probe_lt & k[[i]][,2]<=probe_gt),])
         d<-merge(d,probe[[i]],by="position",all=T)
         d=d[c(-(i+2))]

         probe_image[[i]]<- data.frame(k[[i]][which(k[[i]][,1]==a[j,1] & k[[i]][,2]>=probe_image_lt & k[[i]][,2]<=probe_image_gt),])
         ProbeS <- probe_image[[i]][-1]
         ProbeS[is.na(ProbeS)] <- 0
         write.table(ProbeS, paste(filename[i], a[j,4], "deep.xls", sep="_"),sep="\t",col.names=T,row.names=F,quote=F)
         d_image<-merge(d_image,probe_image[[i]],by="position",all=T)
         d_image=d_image[c(-(i+2))]
         if(max(probe_image[[i]][,3])>gmax){gmax=max(probe_image[[i]][,3])}else {gmax=gmax}

    }
    d=d[c(-2)]
    write.table(d,paste(a[j,4],"_deep.xls",sep=""),sep="\t",col.names=T,row.names=F,quote=F)


    d_image=d_image[c(-2)]
    write.table(d_image,paste(a[j,4],"_image_deep.xls",sep=""),sep="\t",col.names=T,row.names=F,quote=F)

    Color <- c("red","dimgray","goldenrod4","black","maroon","maroon1","mediumorchid","greenyellow","green4","green","yellow","blue","tomato","coral4","slateblue","cornflowerblue","darkred","darkorange","darkorange4","darkorange3","cyan2","cyan4","cornsilk4","darkgoldenrod4","darkgoldenrod1","greenyellow","green4","green","yellow","blue","tomato","coral4","slateblue","cornflowerblue","darkred","darkorange","darkorange4","darkorange3","cyan2","cyan4","cornsilk4","darkgoldenrod4","darkgoldenrod1","red","dimgray","goldenrod4","black","maroon")
    Color <- rep(Color,10)
    Line <- c(1:6,1:6,1:6,1:6,1:6,1:6,1:6,1:6,1:6,1:6,1:6,1:6,1:6,1:6,1:6,1:6,1:6)
    Word <- c(rep(1,96))

    if (a[j,6]=="+"){
    d$len<-c(d$position-a[j,3])
        d[is.na(d)]<-0

        h<-colnames(d)
        h=h[-1]
        h=h[-(sample_sum+1)]
        g=length(h)
        for (e in 1:g){
            eaverage=mean(d[,e+1][1:(a[j,3]-a[j,2])])
            f=(d[,e+1]/eaverage*100)
            d<-cbind(d,f)
            }
        colnames(d)<-c("position",h[1:g],"length",paste(h[1:g],"_rate",sep=""))
        d[is.na(d)]<-0
        write.table(d,paste(a[j,4],"_rate.xls",sep=""),sep="\t",col.names=T,row.names=F,quote=F)
        
        d_image[is.na(d_image)]<-0
        d_image<-d_image[order(d_image$position),]
        num1=nrow(d_image)
        d_image$num1<-c(1:num1)
        CairoJPEG(paste(a[j,4],".jpg",sep=""),width=1200,height=600)
        xrange <- range(d_image$num1)
        yrange <- range(d_image$position)
        lenum<-ceiling(length(filename)/20)
        plot(xrange,yrange,type="n",main=(paste(a[j,4],sep="")),xlab="position",ylab="depth",ylim=c(0,5/4*gmax),cex.axis=2,cex.main=2,cex.lab=2)
        for(i in 1:length(filename)){lines(d_image$num1,d_image[,i+1],type="b",pch=i,lty=Line[i],col=Color[i])}

        f_p=d_image$position[1]
        p1=rep(a[j,2]-f_p+1,5/4*gmax+1)
        q1=c(0:(5/4*gmax))
        r1=data.frame(p1,q1)
        lines(r1$p1,r1$q1,lty=5,lwd=3,col="cyan")

        o1=rep(a[j,3]-f_p+1,(5/4*gmax+1))
        r1=data.frame(o1,q1)
        lines(r1$o1,r1$q1,lty=5,lwd=3,col="cyan")
        text(1/2*(a[j,2]+a[j,3])-f_p+1,1/2*gmax,a[j,4],pos=3,cex=c(1.5),col="red")

        if (a[j,7]==a[j,8]){
            abline(v=a[j,7]-f_p+1,lty=5,col="purple")
            text(a[j,7]-f_p+1,3/4*gmax,a[j,7],pos=4,cex=c(1),col="purple",srt=90)
        }else{
            abline(v=a[j,7]-f_p+1,lty=5,col="purple")
            abline(v=a[j,8]-f_p+1,lty=5,col="purple")
            text(a[j,7]-f_p+1,3/4*gmax,a[j,7],pos=4,cex=c(1),col="purple",srt=90)
            text(a[j,8]-f_p+1,3/4*gmax,a[j,8],pos=2,cex=c(1),col="purple",srt=90)
        }

        legend("topright",inset=.1,title="",c(filename[1:i]),lty=c(Line[1:i]),cex=c(Word[1:i]),pch=c(1:i),col=c(Color[1:i]),ncol=lenum)
        dev.off()
    }else{
            d$len<-c(a[j,2]-d$position)
            d<-d[order(d$len),]
            d[is.na(d)]<-0

            h<-colnames(d)
            h=h[-1]
            h=h[-(sample_sum+1)]
            g=length(h)
            for (e in 1:g){
                eaverage=mean(d[,e+1][1:(a[j,3]-a[j,2])])
                f=(d[,e+1]/eaverage*100)
                d<-cbind(d,f)
            }
        colnames(d)<-c("position",h[1:g],"length",paste(h[1:g],"_rate",sep=""))
        write.table(d,paste(a[j,4],"_rate.xls",sep=""),sep="\t",col.names=T,row.names=F,quote=F)

        d_image[is.na(d_image)]<-0
        d_image<-d_image[order(-d_image$position),]
        num1=nrow(d_image)
        d_image$num1<-c(1:num1)
        CairoJPEG(paste(a[j,4],".jpg",sep=""),width=1200,height=600)
        xrange <- range(d_image$num1)
        yrange <- range(d_image$position)
        lenum<-ceiling(length(filename)/20)
        plot(xrange,yrange,type="n",main=(paste(a[j,4],sep="")),xlab="position",ylab="depth",ylim=c(0,5/4*gmax),cex.axis=2,cex.main=2,cex.lab=2)
        for(i in 1:length(filename)){lines(d_image$num1,d_image[,i+1],type="b",pch=i,lty=Line[i],col=Color[i])}

        f_p=d_image$position[1]
        p1=rep(f_p-a[j,2]+1,5/4*gmax+1)
        q1=c(0:(5/4*gmax))
        r1=data.frame(p1,q1)
        lines(r1$p1,r1$q1,lty=5,lwd=3,col="cyan")

        o1=rep(f_p-a[j,3]+1,(5/4*gmax+1))
        r1=data.frame(o1,q1)
        lines(r1$o1,r1$q1,lty=5,lwd=3,col="cyan")
        text(f_p-1/2*(a[j,2]+a[j,3])+1,1/2*gmax,a[j,4],pos=3,cex=c(1.5),col="red")

        if (a[j,7]==a[j,8]){
            abline(v=f_p-a[j,7]+1,lty=5,col="purple")
            text(f_p-a[j,7]+1,3/4*gmax,a[j,7],pos=4,cex=c(1),col="purple",srt=90)
        }else{
            abline(v=f_p-a[j,7]+1,lty=5,col="purple")
            abline(v=f_p-a[j,8]+1,lty=5,col="purple")
            text(f_p-a[j,7]+1,3/4*gmax,a[j,7],pos=4,cex=c(1),col="purple",srt=90)
            text(f_p-a[j,8]+1,3/4*gmax,a[j,8],pos=2,cex=c(1),col="purple",srt=90)
        }

        legend("topright",inset=.1,title="",c(filename[1:i]),lty=c(Line[1:i]),cex=c(Word[1:i]),pch=c(1:i),col=c(Color[1:i]),lenum)
        dev.off()

    }
}

