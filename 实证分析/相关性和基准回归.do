*********************************小米su7舆情与股票*********************************
//数据导入合并clear
import excel "E:\3-work\0stata\小米su7舆情与股票\每日情感加权分数.xlsx", sheet("Sheet1") firstrow
drop E
save "E:\3-work\0stata\小米su7舆情与股票\x.dta",replace

clear
import excel "E:\3-work\0stata\小米su7舆情与股票\小米集团-W 1810.HK_每日行情数据2.xlsx", sheet("Sheet2") firstrow
merge 1:1 日期 using"E:\3-work\0stata\小米su7舆情与股票\x.dta",keep(3) nogen
save "E:\3-work\0stata\小米su7舆情与股票\xy.dta",replace

import excel "E:\3-work\0stata\小米su7舆情与股票\小米(1).xlsx", sheet("Sheet2") firstrow clear
save "E:\3-work\0stata\小米su7舆情与股票\car.dta",replace

use "E:\3-work\0stata\小米su7舆情与股票\xy.dta",clear
merge 1:1 日期 using"E:\3-work\0stata\小米su7舆情与股票\car.dta",keep(3) nogen
save "E:\3-work\0stata\小米su7舆情与股票\xycar.dta",replace
use "E:\3-work\0stata\小米su7舆情与股票\xycar.dta",clear

**************************尝试*******************
use "E:\3-work\0stata\小米su7舆情与股票\xycar.dta",clear
//相关性尝试
pwcorr_a 预期收益率 超额收益率 累计超额收益率 开盘价 最高价 最低价 收盘价 收盘价前复权 涨跌 涨跌幅 成交量股 成交额 换手率 正面加权分数 负面加权分数 总加权分数 

//回归尝试
reg 换手率 负面加权分数 涨跌幅   开盘价 最高价  收盘价  涨跌幅   换手率  负面加权分数 
gen a=abs(负面加权分数)
reg 换手率 a 


**************************结果*******************
use "E:\3-work\0stata\小米su7舆情与股票\xycar.dta",clear
//调整变量名和量纲
rename (换手率 正面加权分数 负面加权分数) (y x1 x2)

foreach i in   x1 x2{
gen ln`i'=ln(abs(`i'+1))
}
sum  y lnx1 lnx2

//相关性
logout ,save(E:\3-work\0stata\小米su7舆情与股票\相关性分析.rtf) word replace:pwcorr_a y lnx1 lnx2

//基准回归
reg y lnx1 
est store y1
reg y  lnx2
est store y2
esttab y1 y2 using "E:\3-work\0stata\小米su7舆情与股票\换手率基准回归.rtf", b(%6.4f) t(%6.4f) nogap  compress star(* 0.1 ** 0.05 *** 0.01) ar2 replace scalar(N)