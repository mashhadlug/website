----------
title: گزارش جلسه ۱۵۴ گروه کاربران لینوکس مشهد
published: 2014-08-14 18:57:00
layout: page
----------
این جلسه در تاریخ ۱۵ مرداد ماه ۱۳۹۳ در محل شرکت پیشگامان متن باز برگزار شد. مباحثی که در این جلسه به آنها پرداخته شد را در زیر مشاهده خواهید نمود:
<!--more-->
## اخبار نرم‌افزارهای آزاد

در ابتدای جلسه اعضا گروه به گفتگو و بحث در مورد تازه‌ترین اخبار نرم‌افزارهای آزاد پرداختند. در این بحث اخبار به شکل زنده از اینترنت توسط اعضای گروه خوانده شد.

## بررسی سیستم کپچا سایت ADSL مخابرات خراسان رضوی و لاگین اتوماتیک به آن *بیژن ابراهیمی*

آقای بیژن ابراهیمی نحوه‌ی کار سیستم کپچا [سایت ADSL مخابرات خراسان رضوی](http://2020.tci-khorasan.ir) را بررسی کردند. در این قسمت نحوه ایجاد و بدست آوردن کد کپچای استفاده شده از صفحه، نمایش داده شد. به دلیل امکان سوء استفاده این قسمت شامل شرح ماوقع نمی‌شود.

## آموزش رمزگذاری و مخفی‌سازی پرونده‌ها در لینوکس از طریق اسکریپت Tomb *آرش موسوی*
لینوکس به‌طور پیش‌فرض از رمزنگاری پشتیبانی میکنه و ابزارهای خوبی رو برای اینکار در اختیار کاربر قرار داده. [Tomb](https://github.com/dyne/Tomb) یک اسکریپت هست که انجام این کار رو بسیار راحت میکنه. Tomb یک پرونده رمزنگاری شده میسازه که میشه روی سیستم mount کرد و پرونده‌های مختلف رو توش قرار داد.

* ### مزایای Tomb

    - پرونده ساخته شده با Tomb مثل یک پارتیشن معمولی است
    - پرونده Tomb با یک کلید (GnuPG) قابل باز شدن است
    - پرونده‌ی کلید رو میشه جدا از پرونده‌ی Tomb نگهداری کرد (مثلا روی فلش، روی یک سرور دیگه و...)
    - از اونجایی که مونت کردن یک پارتیشن احتیاج به دسترسی sudo داره، پس پسورد کاربر ریشه هم لازم هست
    - میشه تعداد زیادی پرونده Tomb با حجم‌های مختلف ساخت و همه رو مدیریت کرد

* ### نصب

تو آرچ Tomb از طریق AUR قابل نصب هست. می‌تونید از `yaourt` یا هر مدیر بسته دیگه‌ای برای نصبش استفاده کنید. برای توزیع‌های دیگه هم به [این صفحه در مستندات Tomb](https://github.com/dyne/Tomb/blob/master/INSTALL.md) مراجعه کنید. Tomb برای نصب نیاز به `ZSH` داره.

* ### نحوه کار

به طور خلاصه، اول باید یک پرونده Tomb با حجم دلخواه بسازید (به همین میزان حجم میتونید داخل این پرونده، پرونده‌های مختلف خودتون رو ذخیره کنید). بعد یک کلید می‌سازید و برای کلید هم یک رمزعبور تعیین می‌کنید. و در آخر این کلید رو به پرونده Tomb متصل می‌کنید تا از این به بعد این پرونده فقط از طریق این کلید و اون رمزعبور باز خواهد شد.

برای ساخت پرونده‌ی Tomb از دستور `dig`، و از کلید `-a` هم برای مشخص کردن حجم پرونده استفاده می‌کنیم (حجم به مگابایت):

    $ tomb dig -s 128 secret.tomb

این یک پرونده Tomb میسازه به اسم `secret.tomb` با حجم ۱۲۸ مگابایت.

حالا یک کلید میسازیم:

    $ tomb forge secret.tomb.key

با این دستور یک کلید میسازید و در نهایت هم از شما یک رمزعبور میخواد که باید به دلخواه وارد کنید.

کلید رو به پرونده متصل میکنیم:

    $ tomb lock secret.tomb -k secret.tomb.key

حالا برای باز کردن پرونده از دستور `open` استفاده می‌کنیم. برای باز کردن پرونده باید پرونده GPG رو هم با کلید `-k` به فرمان بدیم:

    tomb open secret.tomb -k secret.tomb.key

برای بستن (umount) کردن پرونده از دستور `tomb close` استفاده کنید. بعدا میشه به همین ترتیب برای تغییر اندازه‌ی پرونده از دستور `resize` استفاده کرد. برای اطلاعات بیشتر `man` رو بخونید.

## بررسی تفاوت کپچا و هانی‌پات *رامین نجارباشی*
هانی پات (به انگلیسی: Honeypot) یک منبع سیستم اطلاعاتی با اطلاعات کاذب است که برای مقابله با هکرها و کشف و جمع‌آوری فعالیت‌های غیرمجاز در شبکه‌های رایانه‌ای بر روی شبکه قرار می‌گیرد. اطلاعات بیشتر را از طریق [ویکی پدیا فارسی](http://fa.wikipedia.org/wiki/%D9%87%D8%A7%D9%86%DB%8C_%D9%BE%D8%A7%D8%AA) بخوانید.

## بحث آزاد

در انتهای جلسه افراد گروه به بحث در مورد نرم‌افزارهای آزاد پرداختند.

این جلسه در ساعت ۱۹:۳۰ به پایان رسید. ضمن تشکر از کسانی که ما را برای برگذاری این جلسه همراهی کردند گروه آماده دریافت هرگونه نظر، پیشنهاد و انتقاد شما دوستان و اعضای گروه می‌باشد.
