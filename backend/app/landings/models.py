import os

from django.db import models
from django.utils.text import slugify
from core.utils.mixins import WebPImageMixin


class LandingPage(models.Model):
    title = models.CharField(max_length=255)
    seotitle = models.CharField(max_length=255, blank=True)
    seodescription = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_main = models.BooleanField(default=False, verbose_name="Сделать главной страницей")

    def __str__(self):
        return self.title

class SlugifyOnSaveMixin:
    def save(self, *args, **kwargs):
        if hasattr(self, 'title') and hasattr(self, 'slug'):
            if not self.slug and self.title:
                self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class HeroBlock(WebPImageMixin, models.Model):
    landing = models.OneToOneField(LandingPage, on_delete=models.CASCADE, related_name='hero_block')
    active = models.BooleanField(default=False)
    title = models.CharField(max_length=255, default='Astana <br>Business–Plan')
    slug = models.SlugField(max_length=250, blank=True, default='hero', verbose_name='id')

    subtitle = models.CharField(max_length=500, blank=True, default='Получите готовый бизнес-план для успешного старта и привлечения инвестиций!')
    background_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    cta_annotation = models.CharField(max_length=500, blank=True, default='Закажите проект под ключ для инвесторов')
    cta_button_text = models.CharField(max_length=100, blank=True, default='Заказать проект')
    cta_url = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.make_webp("background_image")

    def webp_url(self):
        if not self.background_image or not self.background_image.name:
            return ""
        url = self.background_image.url
        return os.path.splitext(url)[0] + ".webp"

    def __str__(self):
        return f"Hero: {self.title}"


class BenefitsBlock(WebPImageMixin, SlugifyOnSaveMixin, models.Model):
    landing = models.OneToOneField('LandingPage', on_delete=models.CASCADE, related_name='benefits_block')
    active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=250, blank=True, default='benefits', verbose_name='id (don"t touch)')
    title = models.CharField(max_length=255, default='Benefits info')

    # Карточка 1
    text1 = models.CharField(max_length=255, verbose_name='First benefits')
    svg_icon1 = models.TextField(blank=True, verbose_name='First SVG Path', default='<svg class="size-12 md:size-8" viewBox="0 0 31 31" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11.0871 5.28296C13.0504 1.761 14.0321 0 15.4999 0C16.9678 0 17.9494 1.761 19.9127 5.28296L20.4206 6.19415C20.9781 7.19498 21.2571 7.69543 21.6921 8.02558C22.1272 8.35578 22.6686 8.47833 23.7521 8.72343L24.7384 8.94663C28.5509 9.80926 30.4573 10.2406 30.911 11.699C31.3646 13.1574 30.0647 14.677 27.4659 17.7164L26.7932 18.5027C26.0548 19.3663 25.6854 19.7982 25.5191 20.3324C25.3532 20.8667 25.409 21.4428 25.5206 22.5952L25.6224 23.6443C26.0151 27.6995 26.2119 29.7269 25.0246 30.6285C23.8368 31.5295 22.0523 30.708 18.4826 29.0645L17.5593 28.6393C16.5446 28.1722 16.0378 27.9387 15.4999 27.9387C14.9621 27.9387 14.4552 28.1722 13.4405 28.6393L12.5172 29.0645C8.94758 30.708 7.16302 31.5295 5.97521 30.6285C4.78812 29.7269 4.98456 27.6995 5.37743 23.6443L5.47921 22.5952C5.59081 21.4428 5.64661 20.8667 5.48076 20.3324C5.31439 19.7982 4.94514 19.3663 4.20656 18.5027L3.53412 17.7164C0.93499 14.677 -0.364522 13.1574 0.0890059 11.699C0.542534 10.2406 2.44877 9.80926 6.26144 8.94663L7.24775 8.72343C8.3312 8.47833 8.87266 8.35578 9.30769 8.02558C9.74273 7.69543 10.0217 7.19498 10.5792 6.19415L11.0871 5.28296Z" fill="#684593"></path></svg>')
    # Карточка 2
    text2 = models.CharField(max_length=255, verbose_name='Second benefits')
    svg_icon2 = models.TextField(blank=True, verbose_name='Second SVG Path', default='<svg class="size-12 md:size-8" viewBox="0 0 39 41" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M19.4356 27.6706C8.43767 27.6706 6.48935 16.7097 6.14421 8.01612C6.0482 5.59787 6.0002 4.38874 6.90852 3.27002C7.81686 2.15132 8.90402 1.96789 11.0783 1.60103C13.2246 1.23891 16.0302 0.938965 19.4356 0.938965C22.8413 0.938965 25.6469 1.23891 27.7931 1.60103C29.9674 1.96789 31.0546 2.15132 31.9629 3.27002C32.8712 4.38874 32.8232 5.59787 32.7272 8.01612C32.3822 16.7097 30.4338 27.6706 19.4356 27.6706Z" fill="#684593"></path><path d="M30.2043 20.8388L35.5821 17.8509C37.0188 17.0528 37.7371 16.6537 38.1327 15.9814C38.5284 15.3091 38.5284 14.4874 38.5284 12.8439V12.7054C38.5286 10.7127 38.5286 9.71635 37.9878 8.96626C37.4473 8.21617 36.5021 7.90109 34.6116 7.27095L32.8003 6.66718L32.7681 6.82879C32.7591 7.19018 32.7444 7.58385 32.7272 8.01612C32.5586 12.2634 32.0064 17.0519 30.2043 20.8388Z" fill="#684593"></path><path d="M6.14421 8.01612C6.31284 12.2636 6.86321 17.0522 8.66561 20.8394L3.28676 17.8509C1.85009 17.0528 1.13175 16.6537 0.736141 15.9814C0.340532 15.3091 0.340513 14.4874 0.340455 12.8439V12.7054C0.340398 10.7127 0.340379 9.71635 0.881008 8.96626C1.42164 8.21617 2.36683 7.90109 4.25726 7.27095L6.06855 6.66718L6.10166 6.83274C6.1106 7.19305 6.1271 7.58541 6.14421 8.01612Z" fill="#684593"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M6.54602 39.1271C6.54602 38.3362 7.18718 37.695 7.97808 37.695H30.8909C31.6818 37.695 32.323 38.3362 32.323 39.1271C32.323 39.9179 31.6818 40.5591 30.8909 40.5591H7.97808C7.18718 40.5591 6.54602 39.9179 6.54602 39.1271Z" fill="#684593"></path><path d="M26.0376 37.695H12.8336L13.4004 34.3539C13.5789 33.4613 14.3625 32.819 15.2727 32.819H23.5985C24.5086 32.819 25.2924 33.4613 25.4707 34.3539L26.0376 37.695Z" fill="#684593"></path><path d="M19.4356 27.6706C18.94 27.6706 18.462 27.6487 18.0024 27.6053V32.819H20.8666V27.6053C20.4072 27.6487 19.9309 27.6706 19.4356 27.6706Z" fill="#684593"></path><path d="M17.8037 8.61957C18.5293 7.31798 18.892 6.66718 19.4345 6.66718C19.977 6.66718 20.3398 7.31798 21.0653 8.61957L21.253 8.95631C21.459 9.32618 21.5622 9.51112 21.7229 9.63313C21.8837 9.75516 22.0838 9.80045 22.4842 9.89104L22.8487 9.97352C24.2577 10.2923 24.9622 10.4517 25.1299 10.9907C25.2975 11.5297 24.8171 12.0913 23.8567 13.2145L23.6081 13.5051C23.3352 13.8243 23.1987 13.9838 23.1372 14.1813C23.0759 14.3787 23.0965 14.5916 23.1378 15.0175L23.1754 15.4052C23.3205 16.9039 23.3933 17.6531 22.9545 17.9863C22.5155 18.3193 21.856 18.0157 20.5368 17.4083L20.1956 17.2512C19.8206 17.0786 19.6333 16.9923 19.4345 16.9923C19.2357 16.9923 19.0484 17.0786 18.6734 17.2512L18.3322 17.4083C17.013 18.0157 16.3535 18.3193 15.9145 17.9863C15.4758 17.6531 15.5484 16.9039 15.6936 15.4052L15.7312 15.0175C15.7725 14.5916 15.7931 14.3787 15.7318 14.1813C15.6703 13.9838 15.5338 13.8243 15.2609 13.5051L15.0124 13.2145C14.0518 12.0913 13.5716 11.5297 13.7392 10.9907C13.9068 10.4517 14.6113 10.2923 16.0203 9.97352L16.3848 9.89104C16.7852 9.80045 16.9853 9.75516 17.1461 9.63313C17.3069 9.51112 17.41 9.32618 17.616 8.95631L17.8037 8.61957Z" fill="#F8F9FD"></path></svg>')
    # Карточка 3 (галерея)
    text3 = models.CharField(max_length=255, verbose_name='Third benefits')
    is_gallery3 = models.BooleanField(default=False)
    image1 = models.ImageField(upload_to='benefits/', blank=True, null=True)
    image2 = models.ImageField(upload_to='benefits/', blank=True, null=True)
    image3 = models.ImageField(upload_to='benefits/', blank=True, null=True)
    image4 = models.ImageField(upload_to='benefits/', blank=True, null=True)
    image5 = models.ImageField(upload_to='benefits/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # конвертируем все картинки
        for img_field in ['image1', 'image2', 'image3', 'image4', 'image5']:
            self.make_webp(img_field)

    # Для удобства можно добавить алиасы:
    def webp_url1(self):
        return self.get_webp_url('image1')
    def webp_url2(self):
        return self.get_webp_url('image2')
    def webp_url3(self):
        return self.get_webp_url('image3')
    def webp_url4(self):
        return self.get_webp_url('image4')
    def webp_url5(self):
        return self.get_webp_url('image5')

    def __str__(self):
        return f"Блок преимуществ для {self.landing.title}"

class SolutionsBlock(SlugifyOnSaveMixin, models.Model):
    landing = models.OneToOneField('LandingPage', on_delete=models.CASCADE, related_name='solutions_block')
    active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=250, blank=True, default='solutions')
    title = models.CharField(max_length=255, blank=True, default='Столкнулись с проблемами?')

    utp = models.CharField(max_length=255)
    cta_button_text = models.CharField(max_length=100, blank=True, default='Заказать проект')

    # Карточка 1
    text1 = models.CharField(max_length=255, verbose_name='First Problem text')
    svg_icon1 = models.TextField(blank=True, default='<svg width="34" height="34" viewBox="0 0 34 34" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 15.3334C12.9205 15.3334 13.6667 14.5872 13.6667 13.6667C13.6667 12.7462 12.9205 12 12 12C11.0796 12 10.3334 12.7462 10.3334 13.6667C10.3334 14.5872 11.0796 15.3334 12 15.3334Z" fill="#FF2626"></path><path d="M20.3334 25.3334C20.3334 23.4924 18.841 22 17 22C15.159 22 13.6667 23.4924 13.6667 25.3334H10.3334C10.3334 21.6515 13.3181 18.6667 17 18.6667C20.6819 18.6667 23.6667 21.6515 23.6667 25.3334H20.3334Z" fill="#FF2626"></path><path d="M23.6667 13.6667C23.6667 14.5872 22.9205 15.3334 22 15.3334C21.0795 15.3334 20.3334 14.5872 20.3334 13.6667C20.3334 12.7462 21.0795 12 22 12C22.9205 12 23.6667 12.7462 23.6667 13.6667Z" fill="#FF2626"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M33.6667 17C33.6667 26.2047 26.2047 33.6667 17 33.6667C7.79529 33.6667 0.333374 26.2047 0.333374 17C0.333374 7.79529 7.79529 0.333374 17 0.333374C26.2047 0.333374 33.6667 7.79529 33.6667 17ZM30.3334 17C30.3334 24.3639 24.3639 30.3334 17 30.3334C9.63624 30.3334 3.66671 24.3639 3.66671 17C3.66671 9.63624 9.63624 3.66671 17 3.66671C24.3639 3.66671 30.3334 9.63624 30.3334 17Z" fill="#FF2626"></path></svg>')
    # Карточка 2
    text2 = models.CharField(max_length=255, verbose_name='Second Problem text')
    svg_icon2 = models.TextField(blank=True, default='<svg width="34" height="34" viewBox="0 0 34 34" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 15.3334C12.9205 15.3334 13.6667 14.5872 13.6667 13.6667C13.6667 12.7462 12.9205 12 12 12C11.0796 12 10.3334 12.7462 10.3334 13.6667C10.3334 14.5872 11.0796 15.3334 12 15.3334Z" fill="#FF2626"></path><path d="M20.3334 25.3334C20.3334 23.4924 18.841 22 17 22C15.159 22 13.6667 23.4924 13.6667 25.3334H10.3334C10.3334 21.6515 13.3181 18.6667 17 18.6667C20.6819 18.6667 23.6667 21.6515 23.6667 25.3334H20.3334Z" fill="#FF2626"></path><path d="M23.6667 13.6667C23.6667 14.5872 22.9205 15.3334 22 15.3334C21.0795 15.3334 20.3334 14.5872 20.3334 13.6667C20.3334 12.7462 21.0795 12 22 12C22.9205 12 23.6667 12.7462 23.6667 13.6667Z" fill="#FF2626"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M33.6667 17C33.6667 26.2047 26.2047 33.6667 17 33.6667C7.79529 33.6667 0.333374 26.2047 0.333374 17C0.333374 7.79529 7.79529 0.333374 17 0.333374C26.2047 0.333374 33.6667 7.79529 33.6667 17ZM30.3334 17C30.3334 24.3639 24.3639 30.3334 17 30.3334C9.63624 30.3334 3.66671 24.3639 3.66671 17C3.66671 9.63624 9.63624 3.66671 17 3.66671C24.3639 3.66671 30.3334 9.63624 30.3334 17Z" fill="#FF2626"></path></svg>')
    # Карточка 3 (галерея)
    text3 = models.CharField(max_length=255, verbose_name='Third Problem text')
    svg_icon3 = models.TextField(blank=True, default='<svg width="34" height="34" viewBox="0 0 34 34" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 15.3334C12.9205 15.3334 13.6667 14.5872 13.6667 13.6667C13.6667 12.7462 12.9205 12 12 12C11.0796 12 10.3334 12.7462 10.3334 13.6667C10.3334 14.5872 11.0796 15.3334 12 15.3334Z" fill="#FF2626"></path><path d="M20.3334 25.3334C20.3334 23.4924 18.841 22 17 22C15.159 22 13.6667 23.4924 13.6667 25.3334H10.3334C10.3334 21.6515 13.3181 18.6667 17 18.6667C20.6819 18.6667 23.6667 21.6515 23.6667 25.3334H20.3334Z" fill="#FF2626"></path><path d="M23.6667 13.6667C23.6667 14.5872 22.9205 15.3334 22 15.3334C21.0795 15.3334 20.3334 14.5872 20.3334 13.6667C20.3334 12.7462 21.0795 12 22 12C22.9205 12 23.6667 12.7462 23.6667 13.6667Z" fill="#FF2626"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M33.6667 17C33.6667 26.2047 26.2047 33.6667 17 33.6667C7.79529 33.6667 0.333374 26.2047 0.333374 17C0.333374 7.79529 7.79529 0.333374 17 0.333374C26.2047 0.333374 33.6667 7.79529 33.6667 17ZM30.3334 17C30.3334 24.3639 24.3639 30.3334 17 30.3334C9.63624 30.3334 3.66671 24.3639 3.66671 17C3.66671 9.63624 9.63624 3.66671 17 3.66671C24.3639 3.66671 30.3334 9.63624 30.3334 17Z" fill="#FF2626"></path></svg>')

    def __str__(self):
        return f"Проблемы и решения {self.landing.title}"

class TariffBlock(SlugifyOnSaveMixin, models.Model):
    landing = models.OneToOneField(LandingPage, on_delete=models.CASCADE, related_name='tariff_block')
    slug = models.SlugField(max_length=250, blank=True, default='tariffs')
    title = models.CharField(max_length=255, blank=True, default="Наши тарифы")
    active = models.BooleanField(default=False)
    current = models.CharField(max_length=3, blank=True, default="₸")

    def __str__(self):
        return f"Тарифы для {self.landing.title}"

class TariffCard(models.Model):
    svg_icon = models.TextField(blank=True, default='<svg class="size-10" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.02958 19.4012C5.97501 19.9508 6.3763 20.4405 6.92589 20.4951C7.47547 20.5497 7.96523 20.1484 8.01979 19.5988L6.02958 19.4012ZM15.9802 19.5988C16.0348 20.1484 16.5245 20.5497 17.0741 20.4951C17.6237 20.4405 18.025 19.9508 17.9704 19.4012L15.9802 19.5988ZM20 12C20 16.4183 16.4183 20 12 20V22C17.5228 22 22 17.5228 22 12H20ZM12 20C7.58172 20 4 16.4183 4 12H2C2 17.5228 6.47715 22 12 22V20ZM4 12C4 7.58172 7.58172 4 12 4V2C6.47715 2 2 6.47715 2 12H4ZM12 4C16.4183 4 20 7.58172 20 12H22C22 6.47715 17.5228 2 12 2V4ZM13 10C13 10.5523 12.5523 11 12 11V13C13.6569 13 15 11.6569 15 10H13ZM12 11C11.4477 11 11 10.5523 11 10H9C9 11.6569 10.3431 13 12 13V11ZM11 10C11 9.44772 11.4477 9 12 9V7C10.3431 7 9 8.34315 9 10H11ZM12 9C12.5523 9 13 9.44772 13 10H15C15 8.34315 13.6569 7 12 7V9ZM8.01979 19.5988C8.22038 17.5785 9.92646 16 12 16V14C8.88819 14 6.33072 16.3681 6.02958 19.4012L8.01979 19.5988ZM12 16C14.0735 16 15.7796 17.5785 15.9802 19.5988L17.9704 19.4012C17.6693 16.3681 15.1118 14 12 14V16Z" fill="currentColor"/></svg>')
    block = models.ForeignKey(TariffBlock, on_delete=models.CASCADE, related_name='cards')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.CharField(max_length=100)
    button_text = models.CharField(max_length=100, default="Выбрать тариф")
    button_url = models.URLField(blank=True)
    accent = models.BooleanField(default=False, help_text="Сделать карточку акцентной (выделенной)")
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} (Тариф)"

class TariffProperty(models.Model):
    card = models.ForeignKey(TariffCard, on_delete=models.CASCADE, related_name='properties')
    is_check = models.BooleanField(default=True, verbose_name="Включить галочку")
    name = models.CharField(max_length=100, verbose_name="Свойство")
    value = models.CharField(max_length=255, verbose_name="Значение")

    def __str__(self):
        return f"{self.name}: {self.value}"

class AboutBlock(WebPImageMixin, SlugifyOnSaveMixin, models.Model):
    landing = models.ForeignKey(LandingPage, on_delete=models.CASCADE, related_name='about_block')
    active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=250, blank=True, default='about')

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    subtitle = models.CharField(max_length=100, verbose_name='Заголовок', default='О нас')
    button_text = models.CharField(max_length=100, default="Получить консультацию")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='about/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.make_webp("image")

    def webp_url(self):
        if not self.image or not self.image.name:
            return ""
        url = self.image.url
        return os.path.splitext(url)[0] + ".webp"

    def __str__(self):
        return f"{self.title} (О нас)"

class CasesBlock(SlugifyOnSaveMixin, models.Model):
    landing = models.OneToOneField(LandingPage, on_delete=models.CASCADE, related_name='cases_block')
    active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=250, blank=True, default='cases')

    title = models.CharField(max_length=100, verbose_name='Cases')

    def __str__(self):
        return f"{self.title} (Кейсы)"

class CasesBlockItem(models.Model):
    cases = models.ForeignKey(CasesBlock, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    price = models.CharField(max_length=100)
    current = models.CharField(max_length=3, blank=True, default="₸")

    def __str__(self):
        return f"{self.title}: {self.price}"

class CertificateBlock(SlugifyOnSaveMixin, models.Model):
    landing = models.OneToOneField(LandingPage, on_delete=models.CASCADE, related_name='certificate_block')

    title = models.CharField(max_length=100, verbose_name='Certificates', default='Certificates')
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}'

class CertificateBlockItem(WebPImageMixin, models.Model):
    block = models.ForeignKey(CertificateBlock, on_delete=models.CASCADE, related_name='items')
    image = models.ImageField(upload_to='certificate/', blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, default=None)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.make_webp("image")

    def webp_url(self):
        if not self.image or not self.image.name:
            return ""
        url = self.image.url
        return os.path.splitext(url)[0] + ".webp"

    def __str__(self):
        return f'{self.image} (Сертификат)'

class ClientsBlock(models.Model):
    landing = models.OneToOneField(LandingPage, on_delete=models.CASCADE, related_name='clients_block')
    active = models.BooleanField(default=False)
    clients_list = models.TextField("Список клиентов (каждый с новой строки)", blank=True)

class FaqBlock(SlugifyOnSaveMixin, models.Model):
    landing = models.OneToOneField(LandingPage, on_delete=models.CASCADE, related_name='faq_block')
    active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=250, blank=True, default='faq')
    title = models.CharField(max_length=255, blank=True, default='FAQ')

    def __str__(self):
        return f'{self.title} (FAQ)'

class FaqBlockItem(models.Model):
    block = models.ForeignKey(FaqBlock, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=255, blank=True, default=None)
    description = models.TextField("описание", blank=True)

    def __str__(self):
        return f'Вопрос: {self.title}, Ответ: {self.description}'