when RULE_INIT {
    # Debug logging control.
    # 0 = debug logging off, 1 = debug logging on.
    set static::sql_challenge_debug 1
}
 
when ACCESS_POLICY_AGENT_EVENT {
    if { [ACCESS::policy agent_id] eq "sql_challenge" } {

        # Initialize the iRulesLX extension
        set rpc_handle [ILX::init sql_challenge_extension]
        if { $static::sql_challenge_debug == 1 }{ log local0. "rpc_handle: $rpc_handle" }
   
        # Call the Node.JS and save the iRulesLX response into session vars
        if {[catch {ILX::call $rpc_handle sql_challenge} rpc_response]} {
            log local0.error  "ILX failure: $rpc_response"
            # Send user graceful error message, then exit event
            return
        }

        if { $static::sql_challenge_debug == 1 }{ log local0. "rpc_response: $rpc_response" }

        # Capture the RPC status from the NodeJS call so it can be evaluated in the policy. Any value greater than 0 indicates a problem.
        ACCESS::session data set session.sql_challenge_rpc_status [ lindex $rpc_response 0]
        ACCESS::session data set session.sql_challenge_question [ lindex $rpc_response 1]
        ACCESS::session data set session.sql_challenge_answer [ lindex $rpc_response 2]
    }
}



