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
    public class FetchEventsController : ControllerBase
    {

        private readonly ILogger<FetchEventsController> _logger;

        public FetchEventsController(ILogger<FetchEventsController> logger)
        {
            _logger = logger;
        }

        [HttpGet("{query}")]
        public FetchEventsReply Get(String query)
        {
            FetchEventsRequest fetchReq;
            String cmdEcho = "";
            try {
                fetchReq = JsonSerializer.Deserialize<FetchEventsRequest>(query);
                cmdEcho = JsonSerializer.Serialize(fetchReq);
            } catch {
                return new FetchEventsReply
                {
                    cmd_echo = cmdEcho,
                    error_code = "request_malformed",
                    events = {}
                };
            }

            var sample_event = new EventSchema 
            {
                visit_id = Guid.NewGuid(),
                event_type = "swag",
                time = DateTime.Now,
                time_since_last = DateTime.Now
            };

            return new FetchEventsReply
            {
                cmd_echo = cmdEcho,
                error_code = "ok",
                events = new List<EventSchema> {sample_event, sample_event}
            };
        }
    }
}
