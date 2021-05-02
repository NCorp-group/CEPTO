using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using System.Text.Json;
using System.Text.Json.Serialization;

using CeptoApi.Models;

namespace CeptoApi.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class AuthenticateController: ControllerBase
    {

        private readonly ILogger<AuthenticateController> _logger;

        public AuthenticateController(ILogger<AuthenticateController> logger)
        {
            _logger = logger;
        }

        [HttpGet("{query}")]
        public AuthenticateReply Get(String query)
        {

            AuthenticateRequest authReq;
            String cmdEcho = "";
            try {
                authReq = JsonSerializer.Deserialize<AuthenticateRequest>(query);
                cmdEcho = JsonSerializer.Serialize(authReq);
            } catch {
                return new AuthenticateReply
                {
                    cmd_echo = cmdEcho,
                    error_code = "malformed_request",
                    session_token = Guid.Empty,
                    expiry = DateTime.Now
                };
            }

            if(authReq.user == "admin" && authReq.pwd == "password"){
                return new AuthenticateReply
                {
                    cmd_echo = cmdEcho,
                    error_code = "ok",
                    session_token = Guid.NewGuid(),
                    expiry = DateTime.Now
                };
            }
            return new AuthenticateReply
            {
                cmd_echo = cmdEcho,
                error_code = "incorrect_credentials",
                session_token = Guid.Empty,
                expiry = DateTime.Now
            };
        }
    }
}
