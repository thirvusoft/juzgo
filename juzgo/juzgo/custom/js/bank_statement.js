frappe.ui.form.on('Bank Statement Import', {
    from_date: function(frm) {
        checkForExistingDocuments(frm);
    },
    to_date: function(frm) {
        checkForExistingDocuments(frm);
    },
    bank_account: function(frm) {
        checkForExistingDocuments(frm);
    },
    validate: function(frm) {
        checkForExistingDocuments(frm);
    }
});

function checkForExistingDocuments(frm) {
    // Check if from_date, to_date, and bank_account are set
    if (frm.doc.from_date && frm.doc.to_date && frm.doc.bank_account) {
        // Fetch existing documents with overlapping date ranges for the specified bank account
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Bank Statement Import',
                filters: {
                    bank_account: frm.doc.bank_account,
                    from_date: ['<=', frm.doc.to_date],
                    to_date: ['>=', frm.doc.from_date]
                },
                fields: ['name']
            },
            callback: function(response) {
                if (response.message.length > 0) {
                    // Check if the new date range is completely outside existing date ranges
                    var overlapping = false;
                    var overlappingDocuments = [];
                    for (var i = 0; i < response.message.length; i++) {
                        var existingDoc = response.message[i];
                        if (
                            (frm.doc.from_date >= existingDoc.to_date && frm.doc.to_date >= existingDoc.to_date) ||
                            (frm.doc.from_date <= existingDoc.from_date && frm.doc.to_date <= existingDoc.from_date)
                        ) {
                            overlapping = false;
                        } else {
                            overlapping = true;
                            overlappingDocuments.push(existingDoc.name);
                        }
                    }

                    if (overlapping) {
                        var links = overlappingDocuments.map(function(doc) {
                            return `<a href="/app/bank-statement-import/${doc}">${doc}</a>`;
                        }).join(', ');

                        frappe.msgprint(__("Documents already exist with overlapping date range: {0}", [links]));
                        // You may want to clear the fields or take other actions here
                    }
                }
            }
        });
    }
}
