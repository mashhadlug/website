----------
title: گزارش جلسه ۱۵۶ گروه کاربران لینوکس مشهد
published: 2014-09-13 18:00:00
layout: page
----------
این جلسه در تاریخ ۱۱ شهریور ماه ۱۳۹۳ در محل فرهنگسرای فناوری و رسانه برگزار شد. مباحثی که در این جلسه به آنها پرداخته شد را در زیر مشاهده خواهید نمود:

<!--more-->

## اخبار نرم‌افزارهای آزاد *آرش موسوی*

در ابتدای جلسه اعضا گروه به گفتگو و بحث در مورد تازه‌ترین اخبار نرم‌افزارهای آزاد پرداختند.

## میانبرهای کمکی تاریخچه در Shell *آرش موسوی*

یکسری متغیرها و میانبرها در shell لینوکس هست که کار کردن باهاش رو خیلی ساده‌تر و باحال‌تر میکنه. این میانبرها همه با `!` شروع میشن. یکسری از پرکاربردترین‌هاش رو اینجا میزارم.

* ### متغیرهای کمکی

فرض کنید دستور قبلی که در ترمینال زدیم دستور `du -h directory/example.rb` بوده. با توجه به این دستور، یک مثال نوشتم و خروجی هر کدوم از متغیرهای کمکی در جدول زیر نمایش داده شده:

<table>
<thead>
<tr>
  <th>متغیر</th>
  <th>توضیحات</th>
  <th>نمونه</th>
  <th>خروجی</th>
</tr>
</thead>
<tbody><tr>
  <td><code>!!</code></td>
  <td>فراخوانی دستور قبل</td>
  <td><code>sudo !!</code></td>
  <td><code>sudo du -h directory/example.rb</code></td>
</tr>
<tr>
  <td><code>!*</code></td>
  <td>هر چیزی غیر از نام دستور قبل</td>
  <td>-</td>
  <td><code>-h directory/example.rb</code></td>
</tr>
<tr>
  <td><code>!:n</code></td>
  <td>جدا کردن قسمتn ام</td>
  <td><code>!:1</code></td>
  <td><code>-h</code></td>
</tr>
<tr>
  <td><code>!$</code> یا <code>$_</code></td>
  <td>آخرین قسمت دستور قبل، معمولاpath</td>
  <td><code>!$</code></td>
  <td><code>directory/example.rb</code></td>
</tr>
<tr>
  <td><code>!$:h</code></td>
  <td>قسمت اول path دستور قبل</td>
  <td><code>!$:h</code></td>
  <td><code>directory</code></td>
</tr>
<tr>
  <td><code>!$:t</code></td>
  <td>قسمت آخر path دستور  قبل</td>
  <td><code>!$:t</code></td>
  <td><code>example.rb</code></td>
</tr>
<tr>
  <td><code>!$:r</code></td>
  <td>path بدون پسوند پرونده</td>
  <td><code>!$:r</code></td>
  <td><code>directory/example</code></td>
</tr>
<tr>
  <td><code>!$:t:r</code></td>
  <td>قسمت آخر path بدون پسوند پرونده</td>
  <td><code>!$:t:r</code></td>
  <td><code>example</code></td>
</tr>
<tr>
  <td><code>!$:t:e</code></td>
  <td>نمایش فقط پسوند</td>
  <td><code>!$:t:e</code></td>
  <td><code>rb</code></td>
</tr>
</tbody></table>


نکته: یک توضیح در مورد دستورهایی که با `!$` شروع میشن: می‌تونید به جای `!$` از `!:n` استفاده کنید. مثلا در دستور نمونه ماpath در قسمت دوم است. پس تمامی موارد بالا با `!:2` هم کار میکنه. همیشه ممکنهpath آخرین قسمت دستور نباشه! :)

* ### کجا استفاده میشن؟

معمولا وقتی در دستور بعدی میخواهید به دستور قبلی ارجاع کنین و نمی‌خواید همه چیز رو دوباره تایپ کنید. مثلا اگر یادتون میره جلوی دستور بزنید sudo می‌تونید تو دستور بعد به جای تایپ کردن همه چیز فقط بنویسین `sudo !!`. یا اینکه در دستور بعد میخواین pathای که در دستور قبلی دادید رو دوباره استفاده کنید، یک راه‌اش اینه که کپی کنید و راه دیگه اینه که مثلا `vim $_`. راحت‌تر نیست؟

* ### تفاوت Bash و Zsh

تنها تفاوت اینه که Bash بلافاصله دستور رو اجرا میکنه ولی Zsh دستور رو فقط نمایش میده. برای اینکه Bash هم خودش اجرا نکنه از `:p` استفاده کنید تا فقط نمایش داده بشه. مثلا: `sudo !!:p`. در کل اگه Bash استفاده می‌کنید برید زودتر ---Zsh استفاده کنید :D

* ### اصلاح دستور قبل

فرض کنید در یک دستور غلط املایی دارین. مثلا `du -h examlpe.rb`. برای اصلاح‌اش کافیه دستور زیر رو بزنید:

    ^examlpe^example

shell دستور اصلاح شده رو نمایش میده.

## معرفی ابزار خط فرمانی TaskWarrior *علیرضا حکم‌آبادی*

یک ابزار خط فرمانی برای مدیریت وظایف (tasks) که براساس ایده ToDoList عمل می‌کند.

روش نصب:

    apt-get install task (ubuntu)
    yum install task (fedora)
    pacman -S task (arch)

اطلاعات بیشتر http://taskwarrior.org/download
با تایپ کردن دستور task این ابزار اجرا شده ولیستی از وظایف را نمایش می‌دهد.

    $ task
    ID Age P Description                      Urg
     1 10s H Buy Milk                           6
     2 20s   Read a Book                        0

برخی از دستورات این ابزار:
اضافه کردن وظیفه جدید:
    task add "Read a Book"

اضافه کردن وظیفه جدید به همراه مشخص کردن اولویت آن: 

    task add priority:H "Buy Milk"

شروع به انجام وظیفه با uuid دو:

    task 2 start

اتمام وظیفه با uuid دو:

    task 2 done

پاک کردن وظیفه با uuid یک:

    task 1 delete

تغییر وظیفه شماره یک با اضاف کردن تگ مجازی(Home) و تغییر الویت متوسط: 

    task 1 modify project:Home priority:M "Buy Milk"

تغییر وظیفه شماره دو با اضاف کردن تگ (home & weekend):

    task 2 modify +home +weekend

ایجاد یک وظیفه جدید به صورت دوره‌ای(ابتدای هر ماه میلادیتا تاریخ مشخص شده):

    task add "Pay the rent" due:1st recur:monthly until:2015_03_31

جستجوی تمام وظیفه‌های مشخص شده با تگ مجازی Home:

    task +Home list

برای پیکربندی شخصی ابزار taskwarrior کافیست فایل (taskrc.) را که در مسیر پوشه خانگی قرار دارد را ویرایش کنید. برای کسب اطلاعات بیشتر در زمینه پیکربندی به این لینک راجعه کنید. http://taskwarrior.org/docs/configuration.html

با استفاده از نرم‌افزار Mirakel که برای دستگاه‌های اندرویدی توسعه داده شده است، می‌توانید وظایف موجود در taskwarrior را با دستگاه اندرویدی خود همگام‌ سازی کنید. برای دریافت نرما‌افزار به آدرس http://mirakel.azapps.de/index.html مراجعه کنید.


## بحث آزاد

در انتهای جلسه افراد گروه به بحث در مورد نرم‌افزارهای آزاد پرداختند.

این جلسه در ساعت ۱۹:۳۰ به پایان رسید. ضمن تشکر از کسانی که ما را برای برگذاری این جلسه همراهی کردند گروه آماده دریافت هرگونه نظر، پیشنهاد و انتقاد شما دوستان و اعضای گروه می‌باشد.