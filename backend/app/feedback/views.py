from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Feedback
from .forms import FeedbackForm
from core.utils.telegram import send_telegram_message


class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback/feedback_form.html'
    success_url = reverse_lazy('feedback-success')

    def get_initial(self):
        initial = super().get_initial()
        source = self.request.GET.get("source", "")
        if source:
            initial["source"] = source
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        feedback = self.object  # только что сохранённый объект
        send_telegram_message(
            f"<b>Новая заявка с сайта!</b>\nИмя: {feedback.name}\nТелефон: {feedback.phone}\n Src: {feedback.source or 'Не указан'}"
        )
        return response