----------
title: گزارش جلسه ۱۵۱ام گروه کاربران لینوکس مشهد
published: 2014-06-11 18:33:00
layout: page
----------
این جلسه در تاریخ ۲۱ خرداد ۱۳۹۳ در محل برگزاری جلسات  در آموزشگاه دیتاسنتر شرق برگزار شد. مباحثی که در این جلسه به آنها پرداخته شد را در زیر مشاهده خواهید نمود:

<!--more-->

## خط فرمان: مدیریت دسترسی به حافظه غيريکسان *مهدی عطائیان*
نوما NUMA (مخفف non-uniform memory access) یک طراحی حافظه است که در این طرح هر پروسسور حافظه محلی مخصوص به خود را دارد و هر پروسسور با سرعت بیشتری می‌تواند به حافظه محلی خود نسبت به حافظه غیر محلی دسترسی داشته باشد.
این معماری بیشتر مناسب پروسس‌هایی است که وابسته به یک کاربر یا تسک باشند در نتیجه اجرای پروسس در یک هسته و با یک رم اختصاصی سرعت اجرا را بیشتر می‌کند.
در سیستم‌عامل گنو/لینوکس از ابزار numactl برای کنترل سیاست‌های نومای پروسس‌ها استفاده می‌کنیم.

برای بررسی وضعیت سخت‌افزار NUMA از دستور زیر استفاده می‌کنیم. با دستور زیر می‌توانیم مشخصات پروسسور را مشاهده کنیم. 

	$ numactl --hardware

چنانچه در خروجی دستور تنها ۱ نود مشاهده شد به این معنی است که معماری پروسسور ما نمی‌تواند از numa پشتیبانی کند.

	$numactl  --hardware 
	available: 1 nodes (0)
	node 0 cpus: 0 1 2 3
	node 0 size: 3735 MB
	node 0 free: 172 MB
	node distances:
	node   0 
	  0:  10 

اگر در خروجی بیش از یک نود وجود داشت به این معنی است که پروسسور از numa پشتبیانی می‌کند. 

	$ numactl --hardware 
	available: 2 nodes (0-1)
	node 0 cpus: 0 1 2 3 8 9 10 11
	node 0 size: 16374 MB
	node 0 free: 10935 MB
	node 1 cpus: 4 5 6 7 12 13 14 15
	node 1 size: 16384 MB
	node 1 free: 15298 MB
	node distances:
	node   0   1 
	  0:  10  20 
	  1:  20  10 

در خروجی بالا دو NODE داریم (که با شماره ۰ و ۱ شناخته می‌شوند) در nod شماره ۰ سی‌پی‌یو‌های ۰ و ۱ و ۲ و ۳ و ۸ و ۹ و ۱۰ و ۱۱ قرار دارد. رم اختصاص یافته به نود صفر ۱۶۳۷۴ مگابایت است که از این رم ۱۰۹۳۵ مگا بایت آن آزاد است. اطلاعات نود ۱ نیز به همین شکل تفسیر می‌شود. 

همچنین در جدول node distance سرعت دسترسی هر نود به مموری‌ها مشخص شده است. در این مثال هر نود با سرعت ۱۰ به حافظه اختصاصی خود متصل می‌شود اما نودها با حافظه دیگر نودها با سرعت ۲۰ ارتباط برقرار می‌کند. 

نکته: وضعیت numa را با استفاده از اطلاعات موجود در مسیر /sys نیز می‌توان به دست آورد. 

	# ls /sys/devices/system/node/
	node0/ node1/ 
	# ls /sys/devices/system/node/node0
	compact    memory1    memory112  memory126  memory18  memory39  memory52  memory66  memory8   memory93
	cpu0       memory10   memory113  memory127  memory19  memory4   memory53  memory67  memory80  memory94
	cpu1       memory100  memory114  memory128  memory2   memory40  memory54  memory68  memory81  memory95
	cpu10      memory101  memory115  memory129  memory20  memory41  memory55  memory69  memory82  memory96
	cpu11      memory102  memory116  memory13   memory21  memory42  memory56  memory7   memory83  memory97
	cpu2       memory103  memory117  memory130  memory22  memory43  memory57  memory70  memory84  memory98
	cpu3       memory104  memory118  memory131  memory23  memory44  memory58  memory71  memory85  memory99
	cpu8       memory105  memory119  memory132  memory3   memory45  memory59  memory72  memory86  numastat
	cpu9       memory106  memory12   memory133  memory32  memory46  memory6   memory73  memory87  scan_unevictable_pages
	cpulist    memory107  memory120  memory134  memory33  memory47  memory60  memory74  memory88  vmstat
	cpumap     memory108  memory121  memory135  memory34  memory48  memory61  memory75  memory89
	distance   memory109  memory122  memory14   memory35  memory49  memory62  memory76  memory9
	hugepages  memory11   memory123  memory15   memory36  memory5   memory63  memory77  memory90
	meminfo    memory110  memory124  memory16   memory37  memory50  memory64  memory78  memory91
	memory0    memory111  memory125  memory17   memory38  memory51  memory65  memory79  memory92


برای مشاهده وضعیت NUMA از دستور زیر استفاده می‌کنیم.

	$ numactl --show
	policy: default
	preferred node: current
	physcpubind: 0 1 2 3 
	cpubind: 0 
	nodebind: 0 

دستور numastat برای مشاهده اطلاعات حافظه استفاده می‌شود.

	# numastat  
	                           node0           node1
	numa_hit                 4134896         1809856
	numa_miss                      0               0
	numa_foreign                   0               0
	interleave_hit             12114           12083
	local_node               4134765         1795945
	other_node                   131           13911

با دستور زیر می‌توانیم یک پروسس را در یک نود  و حافظه اجرا کنیم. 

	$ numactl --membind=7 --cpunodebind=7 mongo

با دستور زیر می‌توانیم اجرای صحیح پروسس‌ها بر اساس سیاست numa را بررسی کنیم. 

	$ for i in `ps -ef | awk '{print $2}'`; do taskset -c -p $i; done

سیاست‌های numa چهار نوع است:

	Types of NUMA policy
	Local (default)
	Bound to specific memory nodes
	Interleave
	Preferred


**مثال ۱**:

	$ numactl --interleave=all program -opts args
	$ numactl --cpubind=0 --membind=0,1 program -opts args
	$ numactl --preferred=1
	$ numactl --localalloc /dev/shm/file
	$ numactl --show

**مثال ۲**:

	$ numastat
	/proc/sys/devices/system/node/*/meminfo
	cpuset cgroup
	cpuset.cpus and cpuset.mems tunables

**مثال ۳**:

	$ sudo gcc -o program numac.c -lnuma	
	$ cat nano numa.c 
	#include <numa.h>
	#include <stdio.h> 
	
	int main(int argc, char **argv) {
	   if (numa_available() < 0) {
	      printf("numa_* functions unavailable\n");
	      return 1;
	   }
	   printf("numa_available: %d \n\r", numa_available());
	   printf("numa_num_possible_nodes: %d \n\r", numa_num_possible_nodes	());
	   printf("numa_max_possible_node: %d \n\r", numa_max_possible_node	());
	   printf("numa_num_configured_nodes: %d \n\r", numa_num_configured_nodes());
	   printf("numa_num_configured_cpus: %d \n\r", numa_num_configured_cpus());
	   //   int myInt;
	   //   printf("numa num: ");
	   //   scanf("%d", &myInt);
	   //   printf("numa_node_size: %d \n\r", numa_node_size(myInt, *free)
	}

## گزارش اولین هکاتون اختصاصی مشهدلاگ *رامین نجارباشی*
[اولین هکاتون اختصاصی گروه مشهدلاگ](http://hackathon.mashhadlug.org) با همکاری گروه لینوکس و پایتون مشهد در روزهای ۱۴ الی ۱۵ خرداد ماه ۱۳۹۳ برگزار شد. در این ارائه آقای رامین نجارباشی از اهداف، فلسفه و همچنین مراحل برگزاری هکاتون صحبت کردند. برای مشاهده فایل ارائه می‌توانید به [اینجا]() مراجعه نمایید. همچنین در زیر می‌توانید به اختصار با پروژه‌هایی که در این دوره هکاتون توسعه یافتند آشنا شوید:

* ### پروژه ROI-M *رامین نجارباشی، بیژن ابراهیمی، مهدی عطائیان، صادق*
  پروژه ROI-M، مدیریت نقاط مورد توجه یابحرانی را بعهده دارد. در این پروژه محیط  توسط یکسری حسگر (Sensors) مونیتور می‌شوند. این حسگرها می‌توانند از وضعیت باز و بسته بودن در تا وضعیت روشنایی و حضور افراد در اتاق و یا هر چیز دیگری را رصد کنند. سپس این اطلاعات از طریق رابط وب و REST API در اختیار افراد و برنامه‌نویسان قرار گیرد. سورس برنامه را می‌توانید از [مخزن مشهد‌لاگ](https://github.com/mashhadlug) در گیت‌هاب [مشاهده](https://github.com/mashhadlug/ROI-Monitor) و دانلود نمایید و یا در آپارت فیلم مربوط به عملکرد پروژه را [مشاهده](http://www.aparat.com/v/tLA5x) نمایید. فایل ارائه را نیز می‌توانید از [اینجا](http://www.slideshare.net/ramin311/hackathon-35884121) مشاهده نمایید.

* ### پروژه IronLOIC *مصطفی ستاری، رضا میرزازاده*
  ابزار ‪LOIC‬ ‪(Low Orbit Ion Canon)‬ ابزاری متن‌باز برای تست شبکه است که توسط گروه Anonymous در سال ۲۰۱۱ توسعه داده شد. اعضای تیم geek (آقایان مصطفی شبگرد و رضا میرزازاده) در این هکاتون تصمیم به بهبود عملکرد و همچنین افزایش قابلیت‌های این ابزار گرفتند. حاصل این پروژه IronLOIC شد که سورس این برنامه را می‌توانید از [این آدرس](https://github.com/shabgrd/ironloic) دریافت کنید.
    
## بررسی اسکریپت Webtastic *بیژن ابراهیمی*
در این ارائه با آقای ابراهیمی همراه بودیم تا نگاهی به اسکریپت سایت‌ساز استاتیک مشهدلاگ به نام WebTastic بیاندازیم. در این ارائه ابتدا با تفاوت‌ها، مزایا و معایب سایت‌های داینامیک و استاتیک آشنا شدیم و سپس به بررسی نحوه عملکرد اسکریپت پرداخته شد. همچنین در ادامه قابلیت‌هایی را نیز به کد اضافه کردیم که می‌توان به امکان استفاده از cache برای ساخت فایل‌های ویرایش شده و همچنین ساخت پلاگین pagination اشاره کرد. برای مشاهده سورس‌کُد برنامه و سایت آزمایشی مشهدلاگ می‌توانید به [مخزن مشهدلاگ در گیت‌هاب](https://github.com/mashhadlug/website) مراجعه نمایید. 

## بحث آزاد
در ادامه جلسه و طبق روال معمول، دقایقی از جلسه به بحث آزاد بین اعضای گروه سپری شد. در زیر لیستی از مهم‌ترین موارد مطرح شده را مشاهده خواهید نمود.

* ### پیگیری مسئولیت‌ها و وظایف نیمه‌تمام گروه *علی موسوی*
  پیرو فراخوان قبلی جهت «کمک اعضا به انجام فعالیت‌های در دست اقدام گروه» در لیست پستی گروه، تصمیمات زیر در این راستا گرفته شد. آقای «مهدی عطائیان» مسئولیت پیگیری و مدیریت حساب‌های کاربری مشهدلاگ و آقای «رامین نجارباشی» نیز مسئولیت پیگیری ثبت گروه به عنوان NGO را بعهده گرفتند. برای دریافت اطلاعات بیشتر می‌تواند به صفحه‌ی «[فعالیت‌های در دست اقدام](http://wiki.mashhadlug.org/doku.php?id=%D9%81%D8%B9%D8%A7%D9%84%DB%8C%D8%AA_%D9%87%D8%A7%DB%8C_%D8%AF%D8%B1_%D8%AF%D8%B3%D8%AA_%D8%A7%D9%82%D8%AF%D8%A7%D9%85)» در ویکی گروه مراجعه نمایید. 

این جلسه با توجه به تاخیر نیم ساعتی در شروع، ساعت ۱۹:۵۰ دقیقه خاتمه یافت. ضمن عذرخواهی از دوستان حاضر در جلسه بابت این تاخیر، گروه آماده دریافت هرگونه نظر، پیشنهاد و انتقاد شما دوستان و اعضای گروه می‌باشد.