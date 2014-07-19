----------
title: گزارش جلسه ۱۵۰‌ام گروه کاربران لینوکس مشهد
published: 2014-06-03 13:19:00
layout: page
----------


این جلسه در تاریخ ۰۷ خرداد ۱۳۹۳ در محل برگزاری جلسات  در آموزشگاه دیتاسنتر شرق برگزار شد. مباحثی که در این جلسه به آنها پرداخته شد را در زیر مشاهده خواهید نمود:

<!--more-->

## اخبار دنیای آزاد و متن‌باز *محمدامین جهانی*

این هفته نیز با بررسی اخبار دنیای نرم‌افزارهای آزاد و متن‌باز با آقای جهانی همراه بودیم. در این جلسه اخباری از انتشار نسخه ۳۵ مرورگر کرومیوم و تغییرات کلیدی آن تا انتشار نسخه پایدار سیستم‌عامل SteamOS را بررسی کردیم.

<!--PDF:DELETE_MILLIONS_OF_FILES-->
<!--tags:delete,linux-->
## خط فرمان: حذف میلیون‌ها فایل در یک سیستم لینوکسی *مهدی عطائیان*

در خط فرمان این هفته، آقای عطائیان سناریویی را مطرح کردند که در آن بواسطه وجود تعداد زیادی از فایل‌های (لزوما نه حجیم)، سیستم قادر به ذخیره کردن فایل جدید نمی‌باشد. در این موقعیت بهینه‌ترین راه برای حذف میلیون‌ها میلیون فایل از روی دیسک سخت‌ شما چه می‌باشد؟

‫inode ساختمان داده‌ای است که در فایل‌سیستم لینوکس اطلاعاتی مانند فایل‌ها، دایرکتوری‌ها و سایر خصوصیات فایل‌سیستم را دخیره می‌کند. هر فایل‌سیستم تعداد محدودی inode و در نتیجه میزان مشخصی از فایل‌ها را می‌تواند نگه‌داری کند. چنانچه تعداد فایل‌های یک فایل‌سیستم از میزان مشخصی بیشتر شود، تعداد inodeهای مجاز آن فایل‌سیستم به اتمام می‌رسد و امکان ذخیره و ایجاد تعداد بیشتری فایل وجود ندارد. برای یافتن تعداد inode‌های مجاز از دستور زیر استفاده می‌کنیم.

	$ df -i
	Filesystem       Inodes IUsed    IFree IUse% Mounted on
	rootfs         60506112 32619 60473493    1% /

اطلاعات بیشتر inode را با دستور زیر می‌توان مشاهده کرد.

	# tune2fs -l /dev/sda1 | grep -i inode
	Filesystem features:      has_journal ext_attr resize_inode dir_index filetype needs_recovery sparse_super
	Inode count:              131072
	Free inodes:              131037
	Inodes per group:         2048
	Inode blocks per group:   256
	First inode:              11
	Inode size:              128
	Journal inode:            8
	Journal backup:           inode blocks

این دستور حداکثر تعداد inode قابل اختصاص و inode‌های اختصاص یافته را نشان می‌دهد. 

چنانچه آی‌نودهای فایل سیستم پر شود تنها راه حل مشکل پاک کردن فایل‌ها و دایرکتوری‌ها می‌باشد. راه‌های متفاوتی برای پاک کردن فایل‌ها وجود دارد.
ابتدا باید فایل‌ها را مشاهده کنیم که در خط فرمان با استفاده از دستور ls می‌توانیم این کار را انجام دهیم. اما اگر تعداد فایل‌های یک دایرکتوری از تعداد مشخصی بیشتر باشد اجرای دستور ls بسیار زمان‌بر خواهد بود. در یک دایرکتوری با ۵۱۰۰۰۰ فایل اجرای دستور ls‬ حدود ۳۱ ثانیه زمان خواهد برد.

	$ time ls
	0m31.325s

نکته: برای ایجاد این تعداد فایل در یک دایرکتوری، و تست دستورات این بخش می‌توانید از دستور زیر استفاده کنید.

	$ cd /path/to/temporary/directory/
	$ for i in $(seq 1 510000); do echo "" >> $i.txt; done 

و از طرفی چنانچه بخواهیم سایر خصوصیات مانند زمان ایجاد و یا حجم فایل را مشاهده کنیم باید دستور ls را با پارامتر ‪-l‬ به کار ببریم. این دستور در دایرکتوری‌ای با ۵۱۰۰۰۰ فایل ۱ دقیقه و ۱۱ ثانیه زمان خواهد بود.

	$ time ls -l
	1m11.900s

بهترین راه برای مشاده فایل‌ها استفاده از دستور ls با پارامتر ‪-1‬ است. این دستور فایل‌های یک دایرکتوری با همان تعداد فایل را در حدود ۱۸ ثانیه لیست خواهد کرد.

	$ time ls -1
	0m18.900s

برای پاک کردن فایل‌ها از دستور rm به همراه پارامتر ‪-rf‬ استفاده می‌کنیم.

	$ rm -rf /path/to/directory/*

در لینوکس تعداد آرگومان‌هایی که می‌توان به عنوان پارامتر به هر دستور ارسال کرد محدود است. برای مشاهده این محدودیت در سیستم خود از دستور ریز استفاده می‌کنیم.

	$ getconf ARG_MAX
	2097152

همچنین برای اطلاعات بیشتر درباره دلایل این محدودیت می‌توانید [این مقاله](http://www.in-ulm.de/~mascheck/various/argmax/) را مطالعه نمایید. در نتیجه چنانچه دستور ‪rm -rf *‬ را در دایرکتوری‌ای اجرا کنیم که تعداد فایل‌های آن از حاصل عبارت ‫2097152-4 بیشتر باشد، دستور فوق با خطای `command: Argument list too long` متوقف می‌شود. دلیل این خطا نیز این است که آدرس این فایل‌ها به عنوان آرگومان به دستور rm ارسال می‌شود که در نتیجه از تعداد آرگومان‌های مجاز (که در بالا دیدیم) تجاوز خواهد کرد.

برای رفع این مشکل چند راه متفاوت داریم. در تمامی راه‌حل‌های زیر باید ۵۱۰٫۰۰۰ فایل موجود در یک دایرکتوری را حذف کنیم.

*  **استفاده از دستور find**:

    اجرای دستور اول بیش از ۲۶ دقیقه و دستور دوم حدود ۷ دقیقه زمان خواهد برد.

		$ time find . -type f -exec rm '{}' \;

		$ find . -print0 | xargs -0 rm

*  **استفاده از دستور ls**:
  
    این دستور ۱۹ ثانیه زمان خواهد برد.

		$ ls -1 | xargs rm -f
   
با توجه به نتایج فوق، بهترین و سریع‌ترین راه پاک کردن تعداد زیادی فایل در یک دایرکتوری استفاده از دستور `ls -1 | xargs rm -f` است.

گاهی اوقات تعداد غیر قابل تصوری فایل، می‌تواند اجرای دستور را با مشکل مواجه کند. به عنوان مثال فرض کنیم باید دو میلیاد فایل در یک دایرکتوری را حذف کنیم. از آنجا که مدیریت حجم چنین لیستی از خروجی ممکن است بسیار بیشتر از میزان حافظه قابل دسترس سیستم باشد، اجرای این دستور غیر ممکن جلوه می‌نماید. برای رفع این مشکل ابتدا دستور ls را اجرا می‌کنیم و خروجی دستور را در یک فایل ذخیره می‌کنیم. در مرحله بعد اطلاعات را از فایل می‌خوانیم و با استفاده از دستور xargs و فراخوانی دستور rm فایلها را پاک میکنیم.

	$ ls -1 > file.txt
	$ rm $(<file.txt)
	# -- OR --
	$ xargs rm < file.txt

پانویس: هر چند حذف تعداد زیادی فایل در مدت زمانی کوتاه می‌تواند در نگاه اول بهینه به نظر برسد، ولی باید بیاد داشته باشیم که بهمین ترتیب نیز سیستم را درگیر پروسه سنگین حذف فایل‌هایی خواهیم کرد که `load average` سیستم را بالا خواهد برد که نهایتا «ممکن» است موجب اختلال در عملکرد دیگر سرویس‌ها شود. بنابراین اگر نیاز به انجام چنین کاری بر روی یک سرور production دارید، بهتر است از یکی از روش‌های کُندتر (مانند حلقه for-loop) استفاده کنید. پانویس برگرفته از [این مقاله](http://www.pronego.com/helpdesk/knowledgebase.php?article=59) می‌باشد.

پانویس ۲: محدودیتی که در بالا به آن اشاره شد، در واقع محدودیت حذف فایل نیست بلکه محدودیت ارسال پارامتر به دستورات خط فرمانی می‌باشد. بنابراین به عنوان مثال اگر بخواهیم تمام فایل‌های یک دایرکتوری را حذف می‌کنیم (صرف نظر از تعداد آنها) می‌توان به سادگی دایرکتوری والد را به با دستور `‪rm -rf parent/‬` حذف کرد.

<!--PDF:DELETE_MILLIONS_OF_FILES-->

##  کرنل لینوکس و کامپایل آن *علی موسوی*

در ارائه این هفته با ارائه «کرنل لینوکس و کامپایل آن» همراه آقای موسوی بودیم. گزارش این ارائه به زودی در ادامه این خبر منتشر خواهد شد. برای مشاهده و همچنین دانلود فایل ارائه می‌توانید به [اینجا](http://www.slideshare.net/tuxitop/ss-35300452) مراجعه نمایید.

## بحث آزاد
در ادامه جلسه و طبق روال معمول، دقایقی از جلسه به بحث آزاد بین اعضای گروه سپری شد. در زیر لیستی از مهم‌ترین موارد مطرح شده را مشاهده خواهید نمود.

* ### اعلام نتیجه انتخابات راهبران و انتخاب نفر پنجم گروه راهبران
  در ادامه و نیز با هماهنگی‌ای که بین آقایان «محمدامین جهانی» و «مهدی عطائیان» دو عضو کاندید برای نفر پنجمی گروه راهبران انجام شده بود و با کناره‌گیری آقای عطائیان، پنجمین عضو گروه راهبران نیز انتخاب شد. بدین ترتیب آقای «محمدامین جهانی» به همراه آقایان «آرش موسوی»، «علیرضا حکم‌آبادی»، «رامین نجارباشی» و «علی موسوی» به مدت یکسال از تاریخ ۷ خرداد ۱۳۹۳ به عنوان راهبران مشهدلاگ فعالیت خواهند کرد. آقای «مهدی عطائیان» و «محمدجواد بدیعی» نیز به عنوان اعضای علی‌البدل در صورت نیاز فعالیت خواهند کرد.

* ### آرشیو جلسات *بیژن ابراهیمی*
  با توجه به انتقاد برخی از دوستان از نحوه اعلام برنامه‌های گروه در جلسات پیش‌رو، از دوستان و علاقمندانی که در لیست‌پستی برای ارائه در جلسات آینده اعلام آمادگی می‌کنند خواهش می‌شود ضمن اعلام آمادگی خود، توضیحات مختصر و مفیدی را نیز درباره ماهیت ارائه، پیش‌نیازها و سطح علمی آن در اختیار دیگر دوستان و همچنین مدیران جلسه قرار دهند تا به نحو شایسته‌ای در اخبار گروه منعکس گردد. همچنین دوستانی که در جلسات گروه به هر نحوی ارائه‌ای را برگزار می‌کنند لطفا آمادگی تهیه آرشیو تصویری از دسکتاپ خود را داشته باشند. برای دریافت اطلاعات بیشتر درباره نحوه انجام اینکار می‌توانید به [اینجا](http://wiki.mashhadlug.org/doku.php?id=%D8%AC%D9%84%D8%B3%D8%A7%D8%AA_%DA%AF%D8%B1%D9%88%D9%87:%D8%B1%D8%A7%D9%87%D9%86%D9%85%D8%A7%DB%8C_%D8%A2%D8%B1%D8%B4%DB%8C%D9%88_%D8%A7%D8%B1%D8%A7%D8%A6%D9%87_%D9%87%D8%A7) مراجعه نمایید.

* ### کتابخانه منابع آموزشی گروه کاربران لینوکس مشهد *مجید رمضانپور*
  با توجه به اهدا شدن ۲ کتاب توسط انتشارات O'Reilly به گروه کاربران لینوکس مشهد که توسط پیگیری‌های آقای نجارباشی و در قالب سیاست حمایت از گروه‌های کاربری انتشارات O'Reilly صورت گرفته شده بود، آقای رمضانپور به همراه آقای نجارباشی پیشنهاد ایجاد کتابخانه‌ای برای نگهداری و اهدای محتوای آموزشی مانند کتاب و یا فیلم را مطرح کردند. دوستان و علاقمندان می‌توانند در صورت دلخواه کتاب‌ها و یا فیلم‌های آموزشی خود را به این کتابخانه اهدا کنند تا توسط دیگر اعضای گروه مورد استفاده قرار بگیرد. اطلاعات بیشتر درباره چگونگی اهدا و یا دریافت این منابع به صورت امانتی به زودی از طریق رسانه‌های ارتباطی گروه اعلام خواهند شد.

این جلسه در ساعت ۱۹:۴۰ دقیقه خاتمه یافت. با تشکر از شما، گروه آماده دریافت هرگونه نظر، پیشنهاد و انتقاد شما دوستان و اعضای گروه می‌باشد.