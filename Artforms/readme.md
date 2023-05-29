# ART FORMS WEB APP

**This web app has two users, Artist and Client**
_Client: Will be able to look at various artist shops and submit a commission request upon clicking the shop_
_Client: Will be able to see current requests submitted to artists to see if the request was accepted or denied_

_Artist: Will be able to look at current requests made by clients, can accept or deny request_
_Artist: Will be able to see current personal shops and create or edit them_

**MODELS**
_Shop_ : _artist_, _requests_, title, description, turnover, baseprice
_Request_: _shop_, _client_, contact email, description of request, accepted(boolean)

_Artist_: name, username, _shops_,
_Client_: name, username, _requests_

_Artist_ and _Shop_ will have a one-to-many relationship, a _shop_ can only have one _artist_, an _artist_ can have many _shops_

_Client_ and _Request_ will have a one-to-many relationship as well

_Request_ and _Shop_ will have a one-to-many relationship, _request_ can only have one _shop_, _shop_ can have many _requests_

**Please refer to _unit05_models.png_ for relationship visual aid.**

**Forms**
_Shop_ : modelForm for _Shop_ model

_Request_ : modelForm for _Request_ model

# LOGIN AND REGISTRATION

@unauthenticated_user
*Login* -> _login_
[]logs user in
[]if Group is **Client**, redirect to _client-home_
[]if Group is **Artist**, redirect to _artist-home_

# CLIENT PAGES
@login_required(login_url='login')
@allowed_users(allowed_roles=['client'])
**if not allowed, redirect to unauthorized page with back button**
_Client Home Page_ -> _client-home_
[] Card that directs to current requests from client, _client-view-requests_
[] card that directs to all artists and their shops, _client-view-artists_

_Client Requests Page_ -> _client-view-requests_
[] shows all current requests and their approval status

_Client View Artists Page_ -> _client-view-artists_
[] shows all artists and their shops
[] if shop is selected, directs to make request page, _client-make-request_

_Client Make Request Page_ -> _client-make-request_
[] fill out form for selected shop and submit
[] redirects to _client-view-requests_ upon submit

# ARTIST PAGES
#login_required(login_url='login')
@allowed_users(allowed_roles=['artist'])
**if not allowed, redirect to unauthorized page with back button**
_Artist Home Page_ -> _artist-home_
[] card that allows artist to view their own shops
[] card that allows artist to view requests that were made to the artist

_Artist Requests Page_ -> _artist-view-requests_
[] shows all current requests made to the artist, if request selected, can approve or deny, _artist-approve-request_

_Artists Shops Page_ -> _artist-view-shops_
[] shows all current shops that artist has, can _add shop_ (_artist-add-shop_) or _edit shop_ (_artist-edit-shop_)

_Artist Add Shop Page_ -> _artist-add-shop_
[] artist fills out a _Shop_ form that will be added to artist's shops

_Artist Edit Shop Page_ -> _artist-edit-shop_
[] artist edits current _Shop_, can delete shop as well
