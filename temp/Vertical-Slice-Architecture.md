---
created: 2026-03-02T14:04:04 (UTC +02:00)
tags: []
source: https://www.milanjovanovic.tech/blog/vertical-slice-architecture-structuring-vertical-slices?utm_source=YouTube&utm_medium=social&utm_campaign=23.02.2026
author: Milan Jovanović
---

# Vertical Slice Architecture:

> ## Excerpt
> Are you tired of organizing your project across layers? Vertical Slice Architecture is a compelling alternative to traditional layered architectures.

---
[**Product for Engineers**](https://newsletter.posthog.com/) from PostHog is a newsletter helping engineers improve their product skills. [**Subscribe for free**](https://newsletter.posthog.com/) to get curated advice on building great products, lessons (and mistakes) from PostHog, and deep dives on top startups.

Are you tired of organizing your project across layers?

Vertical Slice Architecture is a compelling alternative to traditional layered architectures. [VSA](https://www.milanjovanovic.tech/blog/vertical-slice-architecture) flips the script on how we structure code.

Instead of horizontal layers (Presentation, Application, Domain), VSA organizes code by feature. Each feature encompasses everything it needs, from API endpoints to data access.

In this newsletter, we will explore how you can structure vertical slices in VSA.

## [Understanding Vertical Slices](https://www.milanjovanovic.tech/blog/vertical-slice-architecture-structuring-vertical-slices?utm_source=YouTube&utm_medium=social&utm_campaign=23.02.2026#understanding-vertical-slices)

At its core, a vertical slice represents a self-contained unit of functionality. It's a slice through the entire application stack. It encapsulates all the code and components necessary to fulfill a specific feature.

In traditional layered architectures, code is organized horizontally across the various layers. One feature implementation can be scattered across many layers. Changing a feature requires modifying the code in multiple layers.

VSA addresses this by grouping all the code for a feature into a single slice.

This shift in perspective brings several advantages:

-   **Improved cohesion**: Code related to a specific feature resides together, making it easier to understand, modify, and test.
-   **Reduced complexity**: VSA simplifies your application's mental model by avoiding the need to navigate multiple layers.
-   **Focus on business logic**: The structure naturally emphasizes the business use case over technical implementation details.
-   **Easier maintenance**: Changes to a feature are localized within its slice, reducing the risk of unintended side effects.

![Vertical slices.](https://www.milanjovanovic.tech/blogs/mnw_092/vertical_slices.png?imwidth=3840)

## [Implementing Vertical Slice Architecture](https://www.milanjovanovic.tech/blog/vertical-slice-architecture-structuring-vertical-slices?utm_source=YouTube&utm_medium=social&utm_campaign=23.02.2026#implementing-vertical-slice-architecture)

Here's an example vertical slice representing the `CreateProduct` feature. We use a static class to represent the feature and group the related types. Each feature can have a respective `Request` and `Response` class. The use case with the business logic can be in a [Minimal API endpoint](https://www.milanjovanovic.tech/blog/automatically-register-minimal-apis-in-aspnetcore).

A vertical slice is likely either a command or a query. This approach gives us [CQRS](https://www.milanjovanovic.tech/blog/cqrs-pattern-with-mediatr) out of the box.

```csharp
public static class CreateProduct
{
    public record Request(string Name, decimal Price);
    public record Response(int Id, string Name, decimal Price);

    public class Endpoint : IEndpoint
    {
        public void MapEndpoint(IEndpointRouteBuilder app)
        {
            app.MapPost("products", Handler).WithTags("Products");
        }

        public static IResult Handler(Request request, AppDbContext context)
        {
            var product = new Product
            {
                Name = request.Name,
                Price = request.Price
            };

            context.Products.Add(product);

            context.SaveChanges();

            return Results.Ok(
                new Response(product.Id, product.Name, product.Price));
        }
    }
}
```

I want to mention a few benefits of structuring your application like this.

The code for the entire `CreateProduct` feature is tightly grouped within a single file. This makes it extremely easy to locate, understand, and modify everything related to this functionality. We don't need to navigate multiple layers (like controllers, services, repositories, etc.).

Directly using `AppDbContext` within the endpoint might tightly couple the slice to your database technology. Depending on your project's size and requirements, you could consider abstracting data access (using a repository pattern) to make the slice more adaptable to changes in the persistence layer.

## [Introducing Validation in Vertical Slices](https://www.milanjovanovic.tech/blog/vertical-slice-architecture-structuring-vertical-slices?utm_source=YouTube&utm_medium=social&utm_campaign=23.02.2026#introducing-validation-in-vertical-slices)

Vertical slices usually need to solve some [cross-cutting concerns](https://www.milanjovanovic.tech/blog/balancing-cross-cutting-concerns-in-clean-architecture), one of which is validation. Validation is the gatekeeper, preventing invalid or malicious data from entering your system. We can easily implement [validation with the FluentValidation library](https://www.milanjovanovic.tech/blog/cqrs-validation-with-mediatr-pipeline-and-fluentvalidation).

Within your slice, you'd define a `Validator` class that encapsulates the rules specific to your feature's request model. It also supports dependency injection, so we can run complex validations here.

```csharp
public class Validator : AbstractValidator<Request>
{
    public Validator()
    {
        RuleFor(x => x.Name).NotEmpty().MaximumLength(100);
        RuleFor(x => x.Price).GreaterThanOrEqualTo(0);
        // ... other rules
    }
}
```

This validator can then be injected into your endpoint using dependency injection, allowing you to perform validation before processing the request.

```csharp
public static class CreateProduct
{
    public record Request(string Name, decimal Price);
    public record Response(int Id, string Name, decimal Price);

    public class Validator : AbstractValidator<Request> // { ... }

    public class Endpoint : IEndpoint
    {
        public void MapEndpoint(IEndpointRouteBuilder app)
        {
            app.MapPost("products", Handler).WithTags("Products");
        }

        public static IResult Handler(
            Request request,
            IValidator<Request> validator,
            AppDbContext context)
        {
            var validationResult = await validator.Validate(request);
            if (!validationResult.IsValid)
            {
                return Results.BadRequest(validationResult.Errors);
            }

            // ... (Create product and return response)
        }
    }
}
```

The previous examples were simple. But what do we do with complex features and shared logic?

VSA excels at managing self-contained features. However, real-world applications often involve complex interactions and shared logic.

Here are a few strategies you can consider to address this:

-   **Decomposition**: Break down complex features into smaller, more manageable vertical slices. Each slice should represent a cohesive piece of the overall feature.
-   **Refactoring**: When a vertical slice becomes difficult to maintain, you can apply some refactoring techniques. The most common ones I use are `Extract method` and `Extract class`.
-   **Extract shared logic**: Identify common logic that's used across multiple features. Create a separate class (or extension method) to reference it from your vertical slices as needed.
-   **Push logic down**: Write vertical slices using procedural code, like a [Transaction Script](https://martinfowler.com/eaaCatalog/transactionScript.html). Then, you can identify parts of the business logic that naturally belong to the domain entities.

You and your team will need to understand code smells and refactorings to make the most of VSA.

## [Summary](https://www.milanjovanovic.tech/blog/vertical-slice-architecture-structuring-vertical-slices?utm_source=YouTube&utm_medium=social&utm_campaign=23.02.2026#summary)

Vertical Slice Architecture is more than just a way to structure your code. By focusing on features, VSA allows you to create cohesive and maintainable applications. Vertical slices are self-contained, making unit and integration testing more straightforward.

VSA brings benefits in terms of code organization and development speed, making it a valuable tool in your toolbox. Code is grouped by feature, making it easier to locate and understand. The structure aligns with the way business users think about features. Changes are localized, reducing the risk of regressions and enabling faster iterations.

Consider embracing [Vertical Slice Architecture](https://www.milanjovanovic.tech/blog/vertical-slice-architecture) in your next project. It's a big mindset shift from [Clean Architecture](https://www.milanjovanovic.tech/pragmatic-clean-architecture). However, they both have their place and even share similar ideas.

That's all for this week. Stay awesome!

___
