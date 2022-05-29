import json

import requests


def dict_filter(obj):
    """
    Filter arguments with not None value
    :return dict
    """
    if obj is None:
        return dict()
    return dict([(k, v) for k, v in obj.items() if v])


class TelegramBotError(Exception):
    pass


class TelegramBot:
    """
    The Bot API is an HTTP-based interface created for developers keen on building 
    bots for Telegram.
    Docs: https://core.telegram.org/bots/api#recent-changes
    """

    MAX_CAPTION_LEN = 1000
    MAX_MESSAGE_LEN = 4000
    MAX_AUDIO_THUMB_SIZE = 320

    def __init__(self, token, server=None):
        if server is None or server[:4] != 'http':
            server = 'https://api.telegram.org'
        self.__server = server
        self.__token = token

    def request(self, method_name, json_body=None, files=None, args=None):
        """
        Send request to telegram api server
        Docs: https://core.telegram.org/bots/api#making-requests

        Returns:
            `result` section from response json if ok or raise TelegramBotError or HTTPError
        """

        if files:
            if json_body and args:
                args = {**json_body, **args}
            elif args is None:
                args = json_body
            json_body = dict()

        response = requests.post(
            url=f'{self.__server}/bot{self.__token}/{method_name}',
            data=dict_filter(args),
            json=dict_filter(json_body),
            files=files,
        )
        try:
            if not response.json().get('ok'):
                raise TelegramBotError(response.json().get('description'))
            return response.json().get('result')
        except json.decoder.JSONDecodeError:
            response.raise_for_status()
            raise TelegramBotError('Not JSON response')

    def set_webhook(self, url, certificate=None, ip_address=None, max_connections=None, allowed_updates=None,
                    drop_pending_updates=None):
        """
        Use this method to specify a url and receive incoming updates via an outgoing
        webhook. Whenever there is an update for the bot, we will send an HTTPS POST
        request to the specified url, containing a JSON-serialized Update. In case of
        an unsuccessful request, we will give up after a reasonable amount of attempts.

        If you'd like to make sure that the Webhook request comes from Telegram, we
        recommend using a secret path in the URL, e.g. https://www.example.com/<token>.
        Since nobody else knows your bot's token, you can be pretty sure it's us.

        Parameter               Type	        Required	Description
        url                     String	        Yes	        HTTPS url to send updates to.
                                                            Use an empty string to remove
                                                            webhook integration
        certificate             InputFile	    Optional	Upload your public key certificate
                                                            so that the root certificate in
                                                            use can be checked. See our
                                                            self-signed guide for details.
        ip_address              String	        Optional	The fixed IP address which will be
                                                            used to send webhook requests instead
                                                            of the IP address resolved through DNS
        max_connections         Integer	        Optional	Maximum allowed number of simultaneous
                                                            HTTPS connections to the webhook for
                                                            update delivery, 1-100. Defaults to 40.
                                                            Use lower values to limit the load on
                                                            your bot's server, and higher values
                                                            to increase your bot's throughput.
        allowed_updates         Array of String Optional	A JSON-serialized list of the update types
                                                            you want your bot to receive. For example,
                                                            specify [“message”, “edited_channel_post”,
                                                            “callback_query”] to only receive updates
                                                            of these types. See Update for a complete
                                                            list of available update types. Specify
                                                            an empty list to receive all update types
                                                            except chat_member (default). If not
                                                            specified, the previous setting will be used.
                                                            Please note that this parameter doesn't
                                                            affect updates created before the call to
                                                            the setWebhook, so unwanted updates may be
                                                            received for a short period of time.
        drop_pending_updates    Boolean	        Optional	Pass True to drop all pending updates

        Returns:
            True on success.
        """
        return self.request('setWebhook', json_body=dict(
            url=url,
            certificate=certificate,
            ip_address=ip_address,
            max_connections=max_connections,
            allowed_updates=allowed_updates,
            drop_pending_updates=drop_pending_updates,
        ))

    def delete_webhook(self, drop_pending_updates=None):
        """
        Use this method to remove webhook integration if you decide to switch back to
        getUpdates.

        Parameter	            Type	Required	Description
        drop_pending_updates	Boolean	Optional	Pass True to drop all pending updates

        Returns:
            True on success.
        """
        return self.request('deleteWebhook', json_body=dict(
            drop_pending_updates=drop_pending_updates
        ))

    def get_me(self):
        """
        A simple method for testing your bot's authentication token.
        Requires no parameters.

        Returns:
            Basic information about the bot in form of a User object.
        """
        return self.request('getMe')

    def send_message(self, chat_id, text, parse_mode=None, entities=None, disable_web_page_preview=None,
                     disable_notification=None, protect_content=None, reply_to_message_id=None,
                     allow_sending_without_reply=None, reply_markup=None):
        """
        Use this method to send text messages.

        Parameter                   Type	                Required    Description
        chat_id	                    Integer or String       Yes         Unique identifier for the target chat or
                                                                        username of the target channel
                                                                        (in the format @channelusername)
        text	                    String                  Yes         Text of the message to be sent, 1-4096
                                                                        characters after entities parsing
        parse_mode                  String                  Optional	Mode for parsing entities in the message text.
                                                                        See formatting options for more details.
        entities                    Array of MessageEntity  Optional	A JSON-serialized list of special entities that
                                                                        appear in message text, which can be specified
                                                                        instead of parse_mode
        disable_web_page_preview	Boolean	                Optional	Disables link previews for links in this message
        disable_notification	    Boolean	                Optional	Sends the message silently. Users will receive
                                                                        a notification with no sound.
        protect_content	            Boolean	                Optional	Protects the contents of the sent message
                                                                        from forwarding and saving
        reply_to_message_id	        Integer	                Optional	If the message is a reply, ID of the
                                                                        original message
        allow_sending_without_reply	Boolean	                Optional	Pass True, if the message should be sent even
                                                                        if the specified replied-to message is not found
        reply_markup                InlineKeyboardMarkup or Optional	Additional interface options. A JSON-serialized
                                    ReplyKeyboardMarkup or              object for an inline keyboard, custom reply
                                    ReplyKeyboardRemove or              keyboard, instructions to remove reply keyboard
                                    ForceReply                          or to force a reply from the user.

        Returns:
            On success, the sent Message is returned.
        """
        return self.request('sendMessage', json_body=dict(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        ))

    def send_photo(self, chat_id, photo, caption=None, parse_mode=None, caption_entities=None, disable_notification=None,
                   protect_content=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        Use this method to send photos.
        Online docs: https://core.telegram.org/bots/api#sendphoto

        Parameter	                Type	                Required	Description
        chat_id	                    Integer or String	    Yes	        Unique identifier for the target chat or
                                                                        username of the target channel
                                                                        (in the format @channelusername)
        photo	                    InputFile or String	    Yes	        Photo to send. Pass a file_id as String to send
                                                                        a photo that exists on the Telegram servers
                                                                        (recommended), pass an HTTP URL as a String for
                                                                        Telegram to get a photo from the Internet, or
                                                                        upload a new photo using multipart/form-data.
                                                                        The photo must be at most 10 MB in size. The
                                                                        photo's width and height must not exceed 10000
                                                                        in total. Width and height ratio must be at
                                                                        most 20. See more info on Sending Files.
        caption	                    String	                Optional	Photo caption (may also be used when resending
                                                                        photos by file_id), 0-1024 characters after
                                                                        entities parsing
        parse_mode	                String	                Optional	Mode for parsing entities in the photo caption.
                                                                        See formatting options for more details.
        caption_entities	        Array of MessageEntity	Optional	A JSON-serialized list of special entities that
                                                                        appear in the caption, which can be specified
                                                                        instead of parse_mode
        disable_notification	    Boolean	                Optional	Sends the message silently. Users will receive
                                                                        a notification with no sound.
        protect_content	            Boolean	                Optional	Protects the contents of the sent message from
                                                                        forwarding and saving
        reply_to_message_id	        Integer	                Optional	If the message is a reply, ID of the original
                                                                        message
        allow_sending_without_reply Boolean	                Optional	Pass True, if the message should be sent even
                                                                        if the specified replied-to message is not found
        reply_markup	            InlineKeyboardMarkup or Optional	Additional interface options. A JSON-serialized
                                    ReplyKeyboardMarkup or              object for an inline keyboard, custom reply
                                    ReplyKeyboardRemove or              keyboard, instructions to remove reply keyboard
                                    ForceReply                          or to force a reply from the user.

        Returns:
            On success, the sent Message is returned.
        """
        data = dict(
            chat_id=chat_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )
        json = files = args = None
        if isinstance(photo, str):
            json = data
            json['photo'] = photo
        else:
            args = data
            files = dict(photo=photo)
        return self.request('sendPhoto', json, files, args)

    def send_audio(self, chat_id, audio, caption=None, parse_mode=None, caption_entities=None, duration=None,
                   performer=None, title=None, thumb=None, disable_notification=None, protect_content=None,
                   reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        Use this method to send audio files, if you want Telegram clients to display
        them in the music player. Your audio must be in the .MP3 or .M4A format.
        Audio files of up to 50 MB in size, this limit may be changed in the future.
        For sending voice messages, use the sendVoice method instead.
        Online docs: https://core.telegram.org/bots/api#sendaudio

        Parameter	                Type	                Required	Description
        chat_id	                    Integer or String	    Yes	        Unique identifier for the target chat or
                                                                        username of the target channel
                                                                        (in the format @channelusername)
        audio	                    InputFile or String	    Yes	        Audio file to send. Pass a file_id as String
                                                                        to send an audio file that exists on the
                                                                        Telegram servers (recommended), pass an HTTP
                                                                        URL as a String for Telegram to get an audio
                                                                        file from the Internet, or upload a new one
                                                                        using multipart/form-data. See more info on
                                                                        Sending Files.
        caption	                    String	                Optional	Audio caption, 0-1024 characters after
                                                                        entities parsing
        parse_mode	                String	                Optional	Mode for parsing entities in the audio caption.
                                                                        See formatting options for more details.
        caption_entities	        Array of MessageEntity	Optional	A JSON-serialized list of special entities that
                                                                        appear in the caption, which can be specified
                                                                        instead of parse_mode
        duration	                Integer	                Optional	Duration of the audio in seconds
        performer	                String	                Optional	Performer
        title	                    String	                Optional	Track name
        thumb	                    InputFile or String	    Optional	Thumbnail of the file sent; can be ignored if
                                                                        thumbnail generation for the file is supported
                                                                        server-side. The thumbnail should be in JPEG
                                                                        format and less than 200 kB in size.
                                                                        A thumbnail's width and height should not
                                                                        exceed 320. Ignored if the file is not uploaded
                                                                        using multipart/form-data. Thumbnails can't be
                                                                        reused and can be only uploaded as a new file,
                                                                        so you can pass “attach://<file_attach_name>”
                                                                        if the thumbnail was uploaded using
                                                                        multipart/form-data under <file_attach_name>.
                                                                        See more info on Sending Files.
        disable_notification	    Boolean	                Optional	Sends the message silently. Users will receive
                                                                        a notification with no sound.
        protect_content	            Boolean	                Optional	Protects the contents of the sent message from
                                                                        forwarding and saving
        reply_to_message_id         Integer	                Optional	If the message is a reply, ID of the
                                                                        original message
        allow_sending_without_reply Boolean	                Optional	Pass True, if the message should be sent even
                                                                        if the specified replied-to message is not found
        reply_markup	            InlineKeyboardMarkup or Optional	Additional interface options. A JSON-serialized
                                    ReplyKeyboardMarkup or              object for an inline keyboard, custom reply
                                    ReplyKeyboardRemove or              keyboard, instructions to remove reply keyboard
                                    ForceReply                          or to force a reply from the user.

        Returns:
            On success, the sent Message is returned. Bots can currently send
        """
        data = dict(
            chat_id=chat_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            performer=performer,
            title=title,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )
        json = files = args = None
        if isinstance(audio, str) and (isinstance(thumb, str) or thumb is None):
            json = data
            json['audio'] = audio
            json['thumb'] = thumb
        elif not isinstance(audio, str) and not isinstance(thumb, str):
            args = data
            files = dict(
                audio=audio,
                thumb=thumb
            )
        elif not isinstance(audio, str):
            args = data
            args['thumb'] = thumb
            files = dict(audio=audio)
        else:
            args = data
            args['audio'] = audio
            files = dict(thumb=thumb)
        return self.request('sendAudio', json, files, args)


class TelegramBotHelper:
    @classmethod
    def split_message(cls, text, first_caption=False, splitter_type=1):
        """
        Split big message (or content caption) to telegram partial messages list,
        considered telegram limitations

        Parameters:
            text (str): Input message for split
            first_caption (bool): Message will be used with captured content?
            splitter_type (int): Character sequence to split input message by blocks:
                -1) split by chars
                0) split by space
                1) split by line (LF char)
                2) split by paragraph (Two LF chars)

        Returns:
            tuple[Caption (str|None), Messages (list[str])]
        """
        messages = cls._split_message(text, first_caption=first_caption, splitter_type=splitter_type)
        if first_caption:
            return messages[0], messages[1:]
        else:
            return None, messages

    @classmethod
    def _split_message(cls, text, first_caption=False, splitter_type=1):
        """
        Split big message (or content caption) to telegram partial messages list,
        considered telegram limitations

        Parameters:
            text (str): Input message for split
            first_caption (bool): Message will be used with captured content?
            splitter_type (int): Character sequence to split input message by blocks:
                -1) split by chars
                0) split by space
                1) split by line (LF char)
                2) split by paragraph (Two LF chars)

        Returns:
            Messages list
        """

        messages = []

        def use_caption():
            return len(messages) == 0 and first_caption

        def max_len():
            return TelegramBot.MAX_CAPTION_LEN if use_caption() else TelegramBot.MAX_MESSAGE_LEN

        # split by characters
        if splitter_type == -1:
            size = TelegramBot.MAX_MESSAGE_LEN
            return [text[:max_len()]] + [text[i:i+size] for i in range(max_len(), len(text), size)]

        # map splitter by splitter_type
        if splitter_type == 0:
            splitter = ' '
        elif splitter_type == 2:
            splitter = '\n\n'
        else:
            splitter = '\n'

        buffer = ''
        # split text, check length of buffered partial message with maximum allowed length and
        # if length is greater flush buffered message to list and reinitialize buffer
        # if partial is greate then maximum allowed length recursive split it with lower splitter type
        for partial in text.split(splitter):
            if (len(buffer) + len(partial) + len(splitter)) < max_len():
                buffer += splitter + partial
            else:
                _trimmed_buffer = buffer.strip()
                if _trimmed_buffer:
                    messages.append(_trimmed_buffer)

                # if partial more than maximum allowed len, split partial by splitter lower type
                if len(partial) > max_len():
                    _messages = cls._split_message(partial, use_caption(), splitter_type=splitter_type - 1)
                    messages.extend(_messages[:-1])
                    buffer = _messages[-1]
                else:
                    buffer = partial

        # append last buffered partial message to answer
        _trimmed_buffer = buffer.strip()
        if _trimmed_buffer:
            messages.append(_trimmed_buffer)

        return messages
