from wechatpy import parse_message,create_reply

def autoreply(request):
    try:
        msg = parse_message(request.body)
        if msg.type == 'text':
            reply = create_reply('这是条文字消息',msg)
        elif msg.type == 'image':
            reply = create_reply('这是条图片消息',msg)
        elif msg.type == 'voice':
            reply = create_reply('这是条语音消息',msg)
        else:
            reply = create_reply('这是条其他类型消息',msg)
        response = HttpResponse(reply.render(),context_type='application/xml')
        return response
    else:
        logger.info('-----------------')  