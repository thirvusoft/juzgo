def add_phone_and_contact(self,action):
    email_ids = []
    if self.primary_email_no and not self.email_id:
        for i in self.email_ids:email_ids.append(i.get('email_id'))
        if self.primary_email_no not in email_ids:
            self.append('email_ids',dict(
                email_id = self.primary_email_no,
                is_primary = 1
            ))
            self.email_id = self.primary_email_no
    phone_nos = []
    if self.primary_mobile_no and not self.mobile_no:
        for i in self.phone_nos:phone_nos.append(i.get('phone'))
        if self.primary_mobile_no not in phone_nos:
            self.append('phone_nos',dict(
                phone = self.primary_mobile_no,
                is_primary_mobile_no = 1
            ))
            self.mobile_no = self.primary_mobile_no
    if self.primary_phone_no and not self.phone:
        if self.primary_phone_no not in phone_nos:
            self.append('phone_nos',dict(
                phone = self.primary_phone_no,
                is_primary_phone = 1
            ))
            self.phone = self.primary_phone_no
