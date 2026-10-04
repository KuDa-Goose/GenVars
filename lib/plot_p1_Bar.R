library(Cairo)
library(RColorBrewer)
                    Plot_tag_Summ <- function(data_s, v, outF) {

                    data1 <- read.table(data_s,  sep="	",  header=T)
                    data  <- as.data.frame(sapply(data1, function(x)as.numeric(gsub("%","",x))))
                    colnames(data1)[1] <- "sample_name"

                    data1[,1] <- gsub("Sample", "", data1[,1])                                                                                          
                    acol <- brewer.pal(12, "Paired")[2]
                    #acol <- adjustcolor(rainbow(10)[8])
                    
                    colnum <- as.numeric(v)
                    
                    #pdf(paste(outF, ".pdf", sep=""), width=10, height=6)   
                    #png(paste(outF, ".png", sep=as.character(v)), res=90, width= 1400, height= 900)
                    CairoPNG(paste(outF, ".png", sep=colnames(data1)[colnum]), res=90, width= 1400, height= 900)
                    
                    par(mar = c(4,8,5,5), oma = c(2,3,3,4))
                    #f <- floor(log(max(data[, colnum]),10)) +1
                    #print(f)
                     
                    tf <- floor(log(max(data[, colnum]),10))+1
                    
                    if(max(data[, colnum]) == 100){
                        max_y <- 100
                        tick_y <- 10
                    } else {
                        tick_y <- ceiling(max(data[, colnum])/10^tf)*10^(tf-1)
                    
                        max_y <- max(data[, colnum]) + tick_y
                    }
                    #print(max_y)
                    #max_y <- 200
                    mainname <- colnames(data)[colnum]
                    barplot(data[,colnum], col=acol, border=acol, ylim=c(0, max_y), xaxt="n", yaxt="n",
                        main= mainname, xlab="Sample Name", ylab="Number")                                      
                    axis(1, at=seq(0.7, 1.2*nrow(data),1.2), label=data1$sample_name,las=3, cex.axis=1.0, tick=F)
                    axis(2, at=seq(0,max_y, tick_y), lab=seq(0,max_y, tick_y),cex.axis = 0.8, las=1)
                    dev.off()

                }
                
                options = commandArgs(TRUE)
                
                data_F = options[1]
                #v_n = options[2]
                oF = options[2]
                d1 <- read.table(data_F,  sep="\t",  header=T)
                for (i in 2:ncol(d1)){
                    percent_da <- as.numeric(gsub("%", "", d1[,i]))
                    if (max(percent_da)>0){
 
                        Plot_tag_Summ(data_F, i, oF)
                    }
                }
                print(warnings()) 
